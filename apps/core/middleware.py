from apps.core.audit import reset_current_request, set_current_request
from apps.core.db import set_institucion_rls


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        parts = host.split(".")
        subdominio = parts[0] if len(parts) > 1 else None
        request.institucion = None

        if subdominio and subdominio not in ["www", "admin", "api", "localhost", "127"]:
            from apps.core.models import Institucion

            try:
                institucion = Institucion.objects.get(subdominio=subdominio, activo=True)
                request.institucion = institucion
                request.session["institucion_id"] = institucion.id
            except Institucion.DoesNotExist:
                request.session.pop("institucion_id", None)

        token = set_current_request(request)
        institucion_id = self._resolve_institucion_id(request)
        set_institucion_rls(institucion_id)
        try:
            return self.get_response(request)
        finally:
            reset_current_request(token)
            set_institucion_rls(None)

    def _resolve_institucion_id(self, request):
        if getattr(request, "institucion", None):
            return request.institucion.id
        if request.user.is_authenticated and request.user.is_superuser:
            return None
        institucion_id = request.session.get("institucion_id")
        if institucion_id:
            return institucion_id
        return None
