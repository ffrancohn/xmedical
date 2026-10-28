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
    if request.user.is_authenticated and not perfil:
        perfil = get_perfil_paciente(request.user, None)
    return {"perfil_paciente": perfil}


def institucion(request):
    tenant = getattr(request, "institucion", None)
    if tenant is None:
        institucion_id = request.session.get("institucion_id")
        if institucion_id:
            tenant = Institucion.objects.filter(id=institucion_id, activo=True).first()
    return {"institucion": tenant}


def visual_preferences(request):
    theme = "garden"
    interface_mode = "classic"
    if request.user.is_authenticated:
        preference = getattr(request.user, "preference", None)
        if preference:
            theme = preference.theme
            interface_mode = preference.interface_mode
    atlas_iso_scene = None
    if interface_mode == "atlas" and request.user.is_authenticated:
        from apps.core.atlas_ui import resolve_atlas_iso_scene

        atlas_iso_scene = resolve_atlas_iso_scene(request)
    atlas_interactive = interface_mode == "atlas" and request.user.is_authenticated
    atlas_nav_active = None
    show_atlas_recepcion_nav = False
    if atlas_interactive:
        profesional = get_profesional(request.user)
        is_recepcion = bool(
            profesional and profesional.tipo == "recepcionista"
        ) or request.user.is_superuser
        match = getattr(request, "resolver_match", None)
        url_name = getattr(match, "url_name", None) or ""
        _nav_urls = {
            "dashboards_recepcion": "recepcion",
            "pacientes_lista": "pacientes",
            "pacientes_nuevo": "pacientes",
            "citas_lista": "citas",
            "citas_agendar": "citas",
            "citas_agendar_flexible": "citas",
        }
        if is_recepcion and url_name in _nav_urls:
            show_atlas_recepcion_nav = True
            atlas_nav_active = _nav_urls[url_name]
    return {
        "visual_theme": theme,
        "interface_mode": interface_mode,
        "atlas_iso_scene": atlas_iso_scene,
        "atlas_interactive": atlas_interactive,
        "show_atlas_recepcion_nav": show_atlas_recepcion_nav,
        "atlas_nav_active": atlas_nav_active,
    }
