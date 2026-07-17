from apps.core.decorators import get_profesional
from apps.core.models import Institucion
from apps.portal_paciente.decorators import get_perfil_paciente


def user_profesional(request):
    return {"profesional": get_profesional(request.user) if request.user.is_authenticated else None}


def user_perfil_paciente(request):
    institucion = getattr(request, "institucion", None)
    if not institucion and request.user.is_authenticated:
        institucion_id = request.session.get("institucion_id")
        if institucion_id:
            institucion = Institucion.objects.filter(id=institucion_id, activo=True).first()
    perfil = (
        get_perfil_paciente(request.user, institucion)
        if request.user.is_authenticated
        else None
    )
    return {"perfil_paciente": perfil}


def institucion(request):
    tenant = getattr(request, "institucion", None)
    if tenant is None:
        institucion_id = request.session.get("institucion_id")
        if institucion_id:
            tenant = Institucion.objects.filter(id=institucion_id, activo=True).first()
    return {"institucion": tenant}


def visual_preferences(request):
    theme = "vital"
    if request.user.is_authenticated:
        preference = getattr(request.user, "preference", None)
        if preference:
            theme = preference.theme
    return {"visual_theme": theme}
