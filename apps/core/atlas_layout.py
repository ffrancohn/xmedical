"""Shell isométrico para formularios y fichas (modo Atlas, legible)."""

from __future__ import annotations

from django.urls import reverse

STAGE_MODULES: dict[str, dict[str, str]] = {
    "pacientes": {
        "icon": "atlas-interactive/assets/v1/modulos/pacientes_archivador_abierto.webp",
        "back_label": "Volver al archivador",
    },
    "citas": {
        "icon": "atlas-interactive/assets/v1/modulos/citas_agenda_abierta.webp",
        "back_label": "Volver a la agenda",
    },
    "historia": {
        "icon": "atlas-interactive/assets/v1/modulos/historia_carpeta_abierta.webp",
        "back_label": "Volver al expediente",
    },
}


def atlas_stage_enabled(request) -> bool:
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return False
    pref = getattr(request.user, "preference", None)
    if not pref or pref.interface_mode != "atlas":
        return False
    return not request.GET.get("classic")


def atlas_stage_context(
    request,
    module_id: str,
    *,
    title: str,
    lead: str = "",
    back_url: str | None = None,
) -> dict:
    if not atlas_stage_enabled(request):
        return {"atlas_stage": False}
    meta = STAGE_MODULES[module_id]
    if back_url is None:
        if module_id == "pacientes":
            back_url = reverse("pacientes_lista") + "?ver=datos"
        elif module_id == "citas":
            back_url = reverse("citas_lista") + "?ver=agenda"
        elif module_id == "historia":
            back_url = reverse("pacientes_lista") + "?ver=datos"
        else:
            back_url = reverse("dashboards_recepcion")
    return {
        "atlas_stage": True,
        "atlas_stage_icon": meta["icon"],
        "atlas_stage_title": title,
        "atlas_stage_lead": lead,
        "atlas_stage_back_url": back_url,
        "atlas_stage_back_label": meta["back_label"],
    }
