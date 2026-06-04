from apps.core.models import Institucion


def institucion(request):
    tenant = getattr(request, "institucion", None)
    if tenant is None:
        institucion_id = request.session.get("institucion_id")
        if institucion_id:
            tenant = Institucion.objects.filter(id=institucion_id, activo=True).first()
    return {"institucion": tenant}


def visual_preferences(request):
    theme = "garden"
    if request.user.is_authenticated:
        preference = getattr(request.user, "preference", None)
        if preference:
            theme = preference.theme
    return {"visual_theme": theme}
