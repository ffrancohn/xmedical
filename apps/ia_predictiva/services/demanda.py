from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Especialidad

from ..config import get_predictiva_config
from ..models import DemandaCita

FRANJAS = [
    ("manana", 6, 12),
    ("tarde", 12, 18),
    ("noche", 18, 22),
]


def _franja_para_hora(hora):
    for nombre, inicio, fin in FRANJAS:
        if inicio <= hora.hour < fin:
            return nombre
    return "otra"


def calcular_demanda_institucion(institucion, dias=90):
    config = get_predictiva_config(institucion)
    if not config["habilitar_demanda"]:
        return 0

    desde = timezone.localdate() - timedelta(days=dias)
    citas = (
        Cita.objects.filter(institucion=institucion, fecha__gte=desde)
        .exclude(estado="cancelada")
        .select_related("profesional__especialidad")
    )

    conteos = defaultdict(int)
    for cita in citas.iterator():
        especialidad = cita.profesional.especialidad
        if not especialidad:
            continue
        franja = _franja_para_hora(cita.hora)
        key = (especialidad.id, cita.fecha.weekday(), franja)
        conteos[key] += 1

    semanas = max(dias / 7, 1)
    actualizadas = 0
    especialidades = Especialidad.objects.filter(institucion=institucion, activo=True)
    for especialidad in especialidades:
        for dia in range(7):
            for franja, _, _ in FRANJAS:
                key = (especialidad.id, dia, franja)
                muestras = conteos.get(key, 0)
                demanda = Decimal(str(round(muestras / semanas, 2)))
                DemandaCita.objects.update_or_create(
                    institucion=institucion,
                    especialidad=especialidad,
                    dia_semana=dia,
                    franja_horaria=franja,
                    defaults={"demanda_esperada": demanda, "muestras": muestras},
                )
                actualizadas += 1
    return actualizadas


def demanda_resumen(instituciones, top=8):
    return (
        DemandaCita.objects.select_related("especialidad", "institucion")
        .filter(institucion__in=instituciones, demanda_esperada__gt=0)
        .order_by("-demanda_esperada")[:top]
    )


def demanda_para_cita(cita):
    especialidad = cita.profesional.especialidad
    if not especialidad:
        return None
    franja = _franja_para_hora(cita.hora)
    return DemandaCita.objects.filter(
        institucion=cita.institucion,
        especialidad=especialidad,
        dia_semana=cita.fecha.weekday(),
        franja_horaria=franja,
    ).first()
