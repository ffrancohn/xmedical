from django import template
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

register = template.Library()


def _can_access(user, profesional, roles):
    if user.is_superuser:
        return True
    if not profesional:
        return False
    return profesional.tipo in roles


def _nav_item(label, url_name, icon, request, profesional, user, roles=None, url_kwargs=None):
    if roles and not _can_access(user, profesional, roles):
        return None
    try:
        url = reverse(url_name, kwargs=url_kwargs or {})
    except NoReverseMatch:
        return None
    path = request.path.rstrip("/") or "/"
    target = url.rstrip("/") or "/"
    active = path == target or path.startswith(f"{target}/")
    icon_html = render_to_string("components/icon.html", {"name": icon})
    return {
        "label": label,
        "url": url,
        "icon_html": mark_safe(icon_html),
        "active": active,
    }


@register.inclusion_tag("components/sidebar_nav.html", takes_context=True)
def sidebar_nav(context):
    request = context["request"]
    user = request.user
    profesional = context.get("profesional")
    perfil_paciente = context.get("perfil_paciente")

    sections = []

    if perfil_paciente and not profesional and not user.is_superuser:
        portal = []
        for item in [
            ("Inicio", "portal_dashboard", "home"),
            ("Mis citas", "portal_citas", "calendar"),
            ("Solicitar cita", "portal_solicitar_cita", "plus-circle"),
            ("Historia clínica", "portal_historia", "file-text"),
        ]:
            nav = _nav_item(item[0], item[1], item[2], request, profesional, user)
            if nav:
                portal.append(nav)
        if portal:
            sections.append({"title": "Portal del paciente", "items": portal})
    else:
        principal = []
        for item in [
            ("Inicio", "dashboard", "home", None),
            ("Pacientes", "pacientes_lista", "users", {"recepcionista", "admin", "medico"}),
            ("Citas", "citas_lista", "calendar", {"recepcionista", "admin", "medico"}),
            ("Preclínica", "preclinica_lista", "heart", {"enfermera", "admin"}),
            ("Referencias", "referencias_lista", "share", {"medico", "admin"}),
        ]:
            nav = _nav_item(item[0], item[1], item[2], request, profesional, user, item[3])
            if nav:
                principal.append(nav)
        if principal:
            sections.append({"title": "Clínica", "items": principal})

        reportes = []
        for item in [
            ("Enfermería", "dashboards_enfermeria", "activity", {"enfermera", "admin"}),
            ("Administración", "dashboards_administracion", "bar-chart", {"admin"}),
            ("Epidemiología", "dashboards_epidemiologia", "trending-up", {"admin"}),
            (
                "Especialista",
                "dashboards_especialista",
                "stethoscope",
                None,
            ),
        ]:
            if item[0] == "Especialista":
                if user.is_superuser or (
                    profesional
                    and profesional.tipo == "medico"
                    and profesional.especialidad
                    and profesional.especialidad.nivel == "segundo"
                ):
                    nav = _nav_item(item[0], item[1], item[2], request, profesional, user)
                    if nav:
                        reportes.append(nav)
            else:
                nav = _nav_item(item[0], item[1], item[2], request, profesional, user, item[3])
                if nav:
                    reportes.append(nav)
        if reportes:
            sections.append({"title": "Reportes", "items": reportes})

    sistema = []
    if perfil_paciente and profesional:
        nav = _nav_item("Portal paciente", "portal_dashboard", "user-circle", request, profesional, user)
        if nav:
            sistema.append(nav)
    if user.is_superuser:
        nav = _nav_item("Superadmin", "superadmin_dashboard", "shield", request, profesional, user)
        if nav:
            sistema.append(nav)
    if _can_access(user, profesional, {"admin"}):
        nav = _nav_item("Auditoría", "auditoria_lista", "file-text", request, profesional, user)
        if nav:
            sistema.append(nav)
    nav = _nav_item("Preferencias", "preferencias_visuales", "settings", request, profesional, user)
    if nav:
        sistema.append(nav)
    if sistema:
        sections.append({"title": "Sistema", "items": sistema})

    return {"sections": sections, "request": request}


@register.inclusion_tag("components/portal_nav.html", takes_context=True)
def portal_nav(context, mobile=False, bottom=False):
    request = context["request"]
    items = []
    for label, url_name in [
        ("Inicio", "portal_dashboard"),
        ("Mis citas", "portal_citas"),
        ("Solicitar cita", "portal_solicitar_cita"),
        ("Historia clínica", "portal_historia"),
        ("Preferencias", "preferencias_visuales"),
    ]:
        url = reverse(url_name)
        path = request.path.rstrip("/") or "/"
        target = url.rstrip("/") or "/"
        items.append(
            {
                "label": label,
                "url": url,
                "active": path == target or path.startswith(f"{target}/"),
            }
        )
    return {"items": items, "request": request, "mobile": mobile, "bottom": bottom}


@register.simple_tag(takes_context=True)
def active_link(context, url_name, *args, **kwargs):
    try:
        url = reverse(url_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return ""
    path = context["request"].path.rstrip("/") or "/"
    target = url.rstrip("/") or "/"
    if path == target or path.startswith(f"{target}/"):
        return "active"
    return ""


@register.inclusion_tag("components/breadcrumbs.html")
def breadcrumbs(items):
    return {"items": items}


@register.inclusion_tag("components/form_field.html")
def form_field(field, help_text=""):
    return {"field": field, "help_text": help_text}


@register.filter
def initials(value):
    parts = str(value or "").split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()
