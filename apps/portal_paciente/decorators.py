from functools import wraps

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from .models import PerfilPaciente


def get_perfil_paciente(user, institucion=None):
    if not user.is_authenticated or user.is_superuser:
        return None
    qs = PerfilPaciente.objects.filter(usuario=user, activo=True).select_related(
        "paciente", "institucion"
    )
    if institucion:
        qs = qs.filter(institucion=institucion)
    return qs.first()


def _resolve_institucion(request):
    institucion = getattr(request, "institucion", None)
    if not institucion:
        from apps.core.views import current_institucion

        institucion = current_institucion(request)
    return institucion


class PacienteRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        institucion = _resolve_institucion(request)
        perfil = get_perfil_paciente(request.user, institucion)
        if not perfil:
            messages.error(request, "No tienes acceso al portal del paciente.")
            return redirect("dashboard")
        request.perfil_paciente = perfil
        return super().dispatch(request, *args, **kwargs)


def paciente_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        institucion = _resolve_institucion(request)
        perfil = get_perfil_paciente(request.user, institucion)
        if not perfil:
            messages.error(request, "No tienes acceso al portal del paciente.")
            return redirect("dashboard")
        request.perfil_paciente = perfil
        return view_func(request, *args, **kwargs)

    return wrapper
