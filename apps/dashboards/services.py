from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.preclinica.models import Preclinica
from apps.referencias.models import Referencia


def _citas_base(instituciones):
    return Cita.objects.select_related("paciente", "profesional", "institucion").filter(institucion__in=instituciones)


def enfermeria_dashboard_data(instituciones, fecha=None):
    fecha = fecha or timezone.localdate()
    citas_hoy = _citas_base(instituciones).filter(fecha=fecha).exclude(estado="cancelada")
    preclinicas_hoy = Preclinica.objects.select_related("cita__paciente", "cita__profesional").filter(
        institucion__in=instituciones,
        cita__fecha=fecha,
    )
    cita_ids_con_preclinica = preclinicas_hoy.values_list("cita_id", flat=True)

    pendientes = citas_hoy.filter(estado__in=["pendiente", "confirmada"]).exclude(id__in=cita_ids_con_preclinica)
    evaluados = citas_hoy.filter(id__in=cita_ids_con_preclinica).order_by("hora")

    alertas_vitales = []
    for preclinica in preclinicas_hoy:
        for mensaje in preclinica.alertas():
            alertas_vitales.append({"preclinica": preclinica, "mensaje": mensaje})

    return {
        "fecha": fecha,
        "pendientes_preclinica": pendientes.order_by("hora"),
        "evaluados_preclinica": evaluados,
        "alertas_vitales": alertas_vitales,
        "total_pendientes": pendientes.count(),
        "total_evaluados": evaluados.count(),
        "total_alertas": len(alertas_vitales),
    }


def administracion_dashboard_data(instituciones, fecha=None):
    fecha = fecha or timezone.localdate()
    inicio_semana = fecha - timedelta(days=6)
    citas_hoy = _citas_base(instituciones).filter(fecha=fecha)
    citas_semana = _citas_base(instituciones).filter(fecha__gte=inicio_semana, fecha__lte=fecha)

    total_hoy = citas_hoy.count()
    activas_hoy = citas_hoy.exclude(estado="cancelada").count()
    canceladas_hoy = citas_hoy.filter(estado="cancelada").count()
    ocupacion = round((activas_hoy / total_hoy) * 100, 1) if total_hoy else 0.0

    total_semana = citas_semana.count()
    canceladas_semana = citas_semana.filter(estado="cancelada").count()
    ausentismo = round((canceladas_semana / total_semana) * 100, 1) if total_semana else 0.0

    consultas_atendidas = Consulta.objects.filter(
        institucion__in=instituciones,
        cita__fecha=fecha,
        cita__estado="atendida",
    ).count()

    return {
        "fecha": fecha,
        "ocupacion_agenda": ocupacion,
        "ausentismo_semana": ausentismo,
        "citas_canceladas_hoy": canceladas_hoy,
        "citas_canceladas_semana": canceladas_semana,
        "consultas_atendidas_hoy": consultas_atendidas,
        "citas_hoy": citas_hoy.order_by("hora"),
        "citas_canceladas_recientes": citas_semana.filter(estado="cancelada").order_by("-fecha", "-hora")[:10],
    }


def especialista_dashboard_data(instituciones, profesional=None, fecha=None):
    fecha = fecha or timezone.localdate()
    referencias = Referencia.objects.select_related(
        "consulta_origen__cita__paciente",
        "especialidad_destino",
        "medico_referente",
        "institucion",
    ).filter(institucion__in=instituciones)

    agenda = Cita.objects.none()
    if profesional:
        if profesional.especialidad_id:
            referencias = referencias.filter(
                Q(estado="pendiente", especialidad_destino=profesional.especialidad)
                | Q(especialista=profesional)
                | Q(medico_referente=profesional)
            )
        else:
            referencias = referencias.filter(Q(especialista=profesional) | Q(medico_referente=profesional))
        agenda = (
            _citas_base(instituciones)
            .filter(profesional=profesional, fecha=fecha)
            .exclude(estado="cancelada")
            .order_by("hora")
        )

    pendientes = referencias.filter(estado="pendiente").order_by("-prioridad", "-creado_en")
    aceptadas = referencias.filter(estado="aceptada").order_by("-creado_en")

    return {
        "fecha": fecha,
        "referencias_pendientes": pendientes,
        "referencias_aceptadas": aceptadas,
        "agenda_propia": agenda,
        "total_pendientes": pendientes.count(),
        "total_aceptadas": aceptadas.count(),
        "total_citas_hoy": agenda.count(),
    }
