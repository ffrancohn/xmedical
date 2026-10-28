"""Catálogo de metáforas isométricas interactivas (Objeto → Exploración → Acción)."""

from __future__ import annotations

from dataclasses import dataclass

from apps.pacientes.views import can_view_pacientes


ASSET_VERSION = "v1"
ASSET_BASE = f"atlas-interactive/assets/{ASSET_VERSION}/modulos"


@dataclass(frozen=True)
class AtlasModule:
    id: str
    label: str
    metaphor: str
    description: str
    asset_closed: str
    asset_open: str


_MODULES: tuple[AtlasModule, ...] = (
    AtlasModule(
        id="pacientes",
        label="Pacientes",
        metaphor="archivador",
        description="Expedientes clínicos y archivador",
        asset_closed=f"{ASSET_BASE}/pacientes_archivador_cerrado.webp",
        asset_open=f"{ASSET_BASE}/pacientes_archivador_abierto.webp",
    ),
    AtlasModule(
        id="citas",
        label="Citas",
        metaphor="agenda",
        description="Agenda, horarios y reservas",
        asset_closed=f"{ASSET_BASE}/citas_agenda_cerrada.webp",
        asset_open=f"{ASSET_BASE}/citas_agenda_abierta.webp",
    ),
    AtlasModule(
        id="flujo_dia",
        label="Atención del día",
        metaphor="mostrador",
        description="Cola y estaciones de recepción",
        asset_closed=f"{ASSET_BASE}/recepcion.webp",
        asset_open=f"{ASSET_BASE}/sala_espera.webp",
    ),
)


def _can_view_citas(user) -> bool:
    return can_view_pacientes(user)


def modules_for_hub(user) -> list[AtlasModule]:
    """Módulos visibles en el hub de recepción según permisos."""
    out: list[AtlasModule] = []
    if can_view_pacientes(user):
        out.append(_MODULES[0])
    if _can_view_citas(user):
        out.append(_MODULES[1])
    out.append(_MODULES[2])
    return out


def module_by_id(module_id: str) -> AtlasModule | None:
    for m in _MODULES:
        if m.id == module_id:
            return m
    return None
