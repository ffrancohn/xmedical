"""Resolución de escena isométrica Atlas según ruta y rol."""

from __future__ import annotations

# url_name → escena por defecto (iso.js)
_ROUTE_SCENES: dict[str, str] = {
    "dashboard": "medico",
    "dashboards_recepcion": "recepcion",
    "dashboards_enfermeria": "enfermeria",
    "dashboards_especialista": "especialista",
    "dashboards_administracion": "admin",
    "superadmin_dashboard": "superadmin",
    "superadmin_backup": "superadmin",
    "configuracion_ia": "admin",
    "preferencias_visuales": "clinic",
    "portal_dashboard": "paciente",
    "pacientes_lista": "recepcion",
    "pacientes_nuevo": "recepcion",
    "pacientes_detalle": "recepcion",
    "pacientes_editar": "recepcion",
    "citas_lista": "recepcion",
    "citas_agendar": "recepcion",
    "citas_agendar_flexible": "recepcion",
}

_ROLE_SCENES: dict[str, str] = {
    "superadmin": "superadmin",
    "administrador": "admin",
    "recepcionista": "recepcion",
    "enfermera": "enfermeria",
    "medico": "medico",
    "especialista": "especialista",
    "paciente": "paciente",
}


def _profesional_role(profesional) -> str | None:
    if profesional is None:
        return None
    tipo = getattr(profesional, "tipo", "") or ""
    mapping = {
        "recepcionista": "recepcion",
        "enfermera": "enfermeria",
        "medico": "medico",
        "especialista": "especialista",
        "administrador": "administrador",
    }
    return mapping.get(tipo)


def resolve_atlas_iso_scene(request) -> str | None:
    """Nombre de escena para ``data-iso``; None si no aplica."""
    match = getattr(request, "resolver_match", None)
    if not match:
        return "clinic"
    url_name = match.url_name or ""
    if url_name in _ROUTE_SCENES:
        return _ROUTE_SCENES[url_name]

    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        if user.is_superuser:
            return "superadmin"
        profesional = getattr(request, "_xm_profesional_cache", None)
        if profesional is None:
            from apps.core.decorators import get_profesional

            profesional = get_profesional(user)
            request._xm_profesional_cache = profesional
        role = _profesional_role(profesional)
        if role and role in _ROLE_SCENES:
            return _ROLE_SCENES[role]
        from apps.portal_paciente.decorators import get_perfil_paciente
        from apps.core.views import current_institucion

        if get_perfil_paciente(user, current_institucion(request)):
            return "paciente"

    return "clinic"
