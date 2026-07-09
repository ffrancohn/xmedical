"""RBAC centralizado por rol de profesional (SEC-P01)."""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from .models import Profesional

ROLE_ADMIN = "admin"
ROLE_MEDICO = "medico"
ROLE_ENFERMERA = "enfermera"
ROLE_RECEPCIONISTA = "recepcionista"

CAN_VIEW_PACIENTES = (ROLE_ADMIN, ROLE_MEDICO, ROLE_ENFERMERA, ROLE_RECEPCIONISTA)
CAN_EDIT_PACIENTES = (ROLE_ADMIN, ROLE_RECEPCIONISTA)
CAN_VIEW_HISTORIA = (ROLE_ADMIN, ROLE_MEDICO)
CAN_CONSULTA = (ROLE_ADMIN, ROLE_MEDICO)
CAN_PRECLINICA = (ROLE_ADMIN, ROLE_ENFERMERA)
CAN_AGENDAR_CITAS = (ROLE_ADMIN, ROLE_RECEPCIONISTA)
CAN_LIST_CITAS = (ROLE_ADMIN, ROLE_RECEPCIONISTA, ROLE_MEDICO)
CAN_CANCELAR_CITAS = (ROLE_ADMIN, ROLE_RECEPCIONISTA, ROLE_MEDICO)
CAN_REFERENCIAS = (ROLE_ADMIN, ROLE_MEDICO)
CAN_AUDITORIA = (ROLE_ADMIN,)
CAN_DASHBOARD_ENFERMERIA = (ROLE_ADMIN, ROLE_ENFERMERA)
CAN_DASHBOARD_ADMIN = (ROLE_ADMIN,)
CAN_DASHBOARD_EPIDEMIOLOGIA = (ROLE_ADMIN,)
CAN_GENERAR_QR = (ROLE_ADMIN, ROLE_MEDICO)


def get_profesional(user):
    if not user.is_authenticated or user.is_superuser:
        return None
    return Profesional.objects.filter(usuario=user, activo=True).select_related("institucion").first()


def user_has_role(user, *roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profesional = get_profesional(user)
    return bool(profesional and profesional.tipo in roles)


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if user_has_role(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para acceder a esta seccion.")
            return redirect("dashboard")

        return wrapper

    return decorator


class RoleRequiredMixin(AccessMixin):
    allowed_roles = ()
    permission_denied_message = "No tienes permiso para acceder a esta seccion."

    def dispatch(self, request, *args, **kwargs):
        if user_has_role(request.user, *self.allowed_roles):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, self.permission_denied_message)
        return redirect("dashboard")


class MedicoRequiredMixin(RoleRequiredMixin):
    allowed_roles = CAN_CONSULTA


class EnfermeraRequiredMixin(RoleRequiredMixin):
    allowed_roles = CAN_PRECLINICA


class RecepcionRequiredMixin(RoleRequiredMixin):
    allowed_roles = CAN_AGENDAR_CITAS


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = CAN_AUDITORIA
