import contextvars
from datetime import date, datetime, time
from decimal import Decimal

from django.forms.models import model_to_dict

from .models import LogAuditoria

_current_request = contextvars.ContextVar("current_request", default=None)

AUDITED_MODELS = {
    "pacientes.Paciente",
    "citas.Cita",
    "preclinica.Preclinica",
    "consulta.Consulta",
    "consulta.Diagnostico",
}


def set_current_request(request):
    return _current_request.set(request)


def reset_current_request(token):
    _current_request.reset(token)


def get_current_request():
    return _current_request.get()


def _json_safe(value):
    if hasattr(value, "pk"):
        return value.pk
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def serialize_instance(instance):
    data = model_to_dict(instance)
    return {key: _json_safe(value) for key, value in data.items()}


def log_audit(instance, accion, valor_anterior=None, valor_nuevo=None, usuario=None, request=None):
    request = request or get_current_request()
    if usuario is None and request and getattr(request, "user", None) and request.user.is_authenticated:
        usuario = request.user

    institucion_id = getattr(instance, "institucion_id", None)
    if not institucion_id:
        return

    ip_address = None
    if request:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            ip_address = forwarded.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")

    LogAuditoria.objects.create(
        institucion_id=institucion_id,
        usuario=usuario,
        accion=accion,
        tabla_afectada=instance._meta.label_lower,
        registro_id=instance.pk,
        valor_anterior=valor_anterior,
        valor_nuevo=valor_nuevo,
        ip_address=ip_address,
    )
