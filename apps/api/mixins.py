from rest_framework.exceptions import PermissionDenied


class InstitucionScopedMixin:
    def get_institucion(self):
        institucion = getattr(self.request, "institucion", None)
        if institucion is None and getattr(self.request, "api_rol", None) != "superadmin":
            raise PermissionDenied("Token sin institucion asociada.")
        return institucion

    def filter_by_institucion(self, queryset):
        institucion = self.get_institucion()
        if institucion is not None:
            return queryset.filter(institucion=institucion)
        return queryset
