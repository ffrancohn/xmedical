from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from apps.citas.models import Cita

from .models import LogNotificacion, RecordatorioMedicamento

ESTADOS_CITA_ACTIVOS = ["pendiente", "confirmada", "en_espera"]
VENTANA_MINUTOS = 30


def recordatorios_activos(institucion) -> bool:
    configuracion = institucion.configuracion or {}
    return configuracion.get("recordatorios_activos", True)


def cita_datetime(cita: Cita):
    tz = timezone.get_current_timezone()
    return timezone.make_aware(datetime.combine(cita.fecha, cita.hora), tz)


def _citas_candidatas():
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=2)
    return (
        Cita.objects.select_related("paciente", "profesional", "institucion")
        .filter(fecha__gte=hoy, fecha__lte=limite, estado__in=ESTADOS_CITA_ACTIVOS)
        .exclude(paciente__email="")
    )


def citas_para_recordatorio(minutos_antes: int):
    now = timezone.localtime()
    objetivo = now + timedelta(minutes=minutos_antes)
    inicio = objetivo - timedelta(minutes=VENTANA_MINUTOS)
    fin = objetivo + timedelta(minutes=VENTANA_MINUTOS)
    citas = []
    for cita in _citas_candidatas():
        if not recordatorios_activos(cita.institucion):
            continue
        dt = cita_datetime(cita)
        if inicio <= dt <= fin:
            citas.append(cita)
    return citas


def ya_notificada_cita(cita: Cita, tipo: str) -> bool:
    return LogNotificacion.objects.filter(cita=cita, tipo=tipo, estado="enviado").exists()


def _registrar_log(**kwargs):
    return LogNotificacion.objects.create(**kwargs)


def enviar_recordatorio_cita(cita: Cita, tipo: str) -> bool:
    if ya_notificada_cita(cita, tipo):
        return False

    paciente = cita.paciente
    if not paciente.email:
        _registrar_log(
            institucion=cita.institucion,
            cita=cita,
            paciente=paciente,
            tipo=tipo,
            destinatario="",
            asunto="",
            estado="omitido",
            detalle="Paciente sin correo electronico",
        )
        return False

    contexto = {
        "paciente": paciente,
        "cita": cita,
        "institucion": cita.institucion,
        "profesional": cita.profesional,
        "tipo": tipo,
    }
    if tipo == "cita_24h":
        asunto = f"Recordatorio: cita manana en {cita.institucion.nombre}"
        template = "email/recordatorio_cita_24h.html"
    else:
        asunto = f"Recordatorio: su cita es en 1 hora - {cita.institucion.nombre}"
        template = "email/recordatorio_cita_1h.html"

    mensaje = render_to_string(template, contexto)
    remitente = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@xmedical.local")

    try:
        send_mail(asunto, mensaje, remitente, [paciente.email], html_message=mensaje, fail_silently=False)
        _registrar_log(
            institucion=cita.institucion,
            cita=cita,
            paciente=paciente,
            tipo=tipo,
            destinatario=paciente.email,
            asunto=asunto,
            estado="enviado",
        )
        return True
    except Exception as exc:
        _registrar_log(
            institucion=cita.institucion,
            cita=cita,
            paciente=paciente,
            tipo=tipo,
            destinatario=paciente.email,
            asunto=asunto,
            estado="fallido",
            detalle=str(exc),
        )
        return False


def _horas_programadas(recordatorio: RecordatorioMedicamento):
    base = recordatorio.hora_recordatorio.hour
    if recordatorio.frecuencia == "diario":
        return {base}
    if recordatorio.frecuencia == "12h":
        return {base, (base + 12) % 24}
    return {base, (base + 8) % 24, (base + 16) % 24}


def _intervalo_minimo_horas(frecuencia: str) -> int:
    return {"diario": 20, "12h": 11, "8h": 7}[frecuencia]


def ya_notificado_medicamento(recordatorio: RecordatorioMedicamento, now=None) -> bool:
    now = now or timezone.now()
    desde = now - timedelta(hours=_intervalo_minimo_horas(recordatorio.frecuencia))
    return LogNotificacion.objects.filter(
        recordatorio_medicamento=recordatorio,
        tipo="medicamento",
        estado="enviado",
        creado_en__gte=desde,
    ).exists()


def medicamentos_para_recordatorio(now=None):
    now = now or timezone.localtime()
    hora_actual = now.hour
    candidatos = RecordatorioMedicamento.objects.select_related("paciente", "institucion").filter(
        activo=True,
    ).exclude(paciente__email="")

    pendientes = []
    for recordatorio in candidatos:
        if not recordatorios_activos(recordatorio.institucion):
            continue
        horas = _horas_programadas(recordatorio)
        if hora_actual not in horas and (hora_actual - 1) % 24 not in horas:
            continue
        if ya_notificado_medicamento(recordatorio, timezone.now()):
            continue
        pendientes.append(recordatorio)
    return pendientes


def enviar_recordatorio_medicamento(recordatorio: RecordatorioMedicamento) -> bool:
    if ya_notificado_medicamento(recordatorio, timezone.now()):
        return False

    paciente = recordatorio.paciente
    if not paciente.email:
        _registrar_log(
            institucion=recordatorio.institucion,
            paciente=paciente,
            recordatorio_medicamento=recordatorio,
            tipo="medicamento",
            destinatario="",
            asunto="",
            estado="omitido",
            detalle="Paciente sin correo electronico",
        )
        return False

    asunto = f"Recordatorio de medicamento - {recordatorio.institucion.nombre}"
    mensaje = render_to_string(
        "email/recordatorio_medicamento.html",
        {
            "paciente": paciente,
            "recordatorio": recordatorio,
            "institucion": recordatorio.institucion,
        },
    )
    remitente = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@xmedical.local")

    try:
        send_mail(asunto, mensaje, remitente, [paciente.email], html_message=mensaje, fail_silently=False)
        _registrar_log(
            institucion=recordatorio.institucion,
            paciente=paciente,
            recordatorio_medicamento=recordatorio,
            tipo="medicamento",
            destinatario=paciente.email,
            asunto=asunto,
            estado="enviado",
        )
        return True
    except Exception as exc:
        _registrar_log(
            institucion=recordatorio.institucion,
            paciente=paciente,
            recordatorio_medicamento=recordatorio,
            tipo="medicamento",
            destinatario=paciente.email,
            asunto=asunto,
            estado="fallido",
            detalle=str(exc),
        )
        return False


def procesar_recordatorios_citas():
    enviados = {"cita_24h": 0, "cita_1h": 0}
    for cita in citas_para_recordatorio(24 * 60):
        if enviar_recordatorio_cita(cita, "cita_24h"):
            enviados["cita_24h"] += 1
    for cita in citas_para_recordatorio(60):
        if enviar_recordatorio_cita(cita, "cita_1h"):
            enviados["cita_1h"] += 1
    return enviados


def procesar_recordatorios_medicamentos():
    enviados = 0
    for recordatorio in medicamentos_para_recordatorio():
        if enviar_recordatorio_medicamento(recordatorio):
            enviados += 1
    return enviados
