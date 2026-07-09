from rest_framework.permissions import BasePermission

from apps.core.permissions import user_has_role


class HasAPIRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        roles = getattr(view, "allowed_roles", None) or self.allowed_roles
        if not roles:
            return True
        if getattr(request, "api_rol", None) == "superadmin":
            return True
        return user_has_role(request.user, *roles)


class IsRecepcionistaAPI(HasAPIRole):
    allowed_roles = ("recepcionista", "admin")


class IsMedicoAPI(HasAPIRole):
    allowed_roles = ("medico", "admin")


class IsEnfermeraAPI(HasAPIRole):
    allowed_roles = ("enfermera", "admin")


class IsClinicalStaffAPI(HasAPIRole):
    allowed_roles = ("recepcionista", "medico", "enfermera", "admin")
