class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        parts = host.split(".")
        subdominio = parts[0] if len(parts) > 1 else None
        request.institucion = None

        if subdominio and subdominio not in ["www", "admin", "api"]:
            from apps.core.models import Institucion

            try:
                institucion = Institucion.objects.get(subdominio=subdominio, activo=True)
                request.institucion = institucion
                request.session["institucion_id"] = institucion.id
            except Institucion.DoesNotExist:
                request.session.pop("institucion_id", None)

        return self.get_response(request)
