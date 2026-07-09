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
        jwt_institucion_id = self._institucion_id_from_jwt(request)
        if jwt_institucion_id is not None:
            return jwt_institucion_id
        if getattr(request, "institucion", None):
            return request.institucion.id
        if request.user.is_authenticated and request.user.is_superuser:
            return None
        institucion_id = request.session.get("institucion_id")
        if institucion_id:
            return institucion_id
        return None

    def _institucion_id_from_jwt(self, request):
        if not request.path.startswith("/api/"):
            return None
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None
        try:
            from rest_framework_simplejwt.authentication import JWTAuthentication

            jwt_auth = JWTAuthentication()
            header = jwt_auth.get_header(request)
            raw_token = jwt_auth.get_raw_token(header)
            if raw_token is None:
                return None
            validated = jwt_auth.get_validated_token(raw_token)
            request.api_rol = validated.get("rol")
            institucion_id = validated.get("institucion_id")
            if institucion_id:
                from apps.core.models import Institucion

                request.institucion = Institucion.objects.filter(pk=institucion_id, activo=True).first()
            return institucion_id
        except Exception:
            return None
