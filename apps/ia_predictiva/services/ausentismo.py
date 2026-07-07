from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Q
from django.utils import timezone

from apps.citas.models import Cita

from ..config import get_predictiva_config, nivel_desde_probabilidad
from ..models import PrediccionAusentismo


def _tasa_cancelacion_paciente(paciente, institucion, antes_de=None):
    qs = Cita.objects.filter(paciente=paciente, institucion=institucion)
    if antes_de:
        qs = qs.filter(creado_en__lt=antes_de)
    total = qs.count()
    if total == 0:
        return None
    canceladas = qs.filter(estado="cancelada").count()
    return canceladas / total


def _tasa_cancelacion_institucion(institucion, dias=90):
    desde = timezone.localdate() - timedelta(days=dias)
    qs = Cita.objects.filter(institucion=institucion, fecha__gte=desde)
    total = qs.count()
    if total == 0:
        return 0.2
    return qs.filter(estado="cancelada").count() / total


def calcular_probabilidad_ausentismo(cita):
    config = get_predictiva_config(cita.institucion)
    factores = {}
    puntos = Decimal("0")

    base = _tasa_cancelacion_institucion(cita.institucion)
    puntos += Decimal(str(round(base * 30, 2)))
    factores["tasa_institucion"] = round(base * 100, 1)

    tasa_paciente = _tasa_cancelacion_paciente(cita.paciente, cita.institucion, cita.creado_en)
    if tasa_paciente is None:
        puntos += Decimal("15")
        factores["historial_paciente"] = "sin historial"
    else:
        puntos += Decimal(str(round(tasa_paciente * 40, 2)))
        factores["historial_paciente"] = round(tasa_paciente * 100, 1)

    if cita.tipo_agendamiento == "flexible":
        puntos += Decimal("10")
        factores["tipo_agendamiento"] = "flexible"

    if cita.hora.hour < 9:
        puntos += Decimal("5")
        factores["hora_temprana"] = True

    if cita.fecha.weekday() >= 5:
        puntos += Decimal("10")
        factores["fin_de_semana"] = True

    dias_anticipacion = (cita.fecha - timezone.localdate()).days
    if dias_anticipacion > 7:
        puntos += Decimal("5")
        factores["anticipacion_dias"] = dias_anticipacion

    if cita.estado == "pendiente":
        puntos += Decimal("5")
        factores["estado_pendiente"] = True

    probabilidad = min(Decimal("100"), max(Decimal("0"), puntos))
    nivel = nivel_desde_probabilidad(probabilidad, config)
    factores["probabilidad"] = float(probabilidad)
    return probabilidad, nivel, factores


def guardar_prediccion_ausentismo(cita):
    config = get_predictiva_config(cita.institucion)
    if not config["habilitar_ausentismo"]:
        return None
    if cita.estado in ("cancelada", "atendida"):
        PrediccionAusentismo.objects.filter(cita=cita).delete()
        return None

    probabilidad, nivel, factores = calcular_probabilidad_ausentismo(cita)
    prediccion, _ = PrediccionAusentismo.objects.update_or_create(
        cita=cita,
        defaults={
            "institucion": cita.institucion,
            "probabilidad": probabilidad,
            "nivel": nivel,
            "factores": factores,
        },
    )
    return prediccion


def predicciones_alerta(instituciones, fecha=None):
    fecha = fecha or timezone.localdate()
    return (
        PrediccionAusentismo.objects.select_related(
            "cita__paciente", "cita__profesional", "cita__profesional__especialidad"
        )
        .filter(institucion__in=instituciones, cita__fecha__gte=fecha, nivel="alto")
        .exclude(cita__estado__in=["cancelada", "atendida"])
        .order_by("-probabilidad")
    )


def reentrenar_ausentismo_institucion(institucion):
    desde = timezone.localdate() - timedelta(days=30)
    citas = Cita.objects.filter(
        institucion=institucion,
        fecha__gte=desde,
    ).exclude(estado__in=["cancelada", "atendida"])
    actualizadas = 0
    for cita in citas.iterator():
        guardar_prediccion_ausentismo(cita)
        actualizadas += 1
    return actualizadas
