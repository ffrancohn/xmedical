"""Catálogo de metáforas isométricas interactivas (Objeto → Exploración → Acción).

Cada área funcional (recepción, médico, especialista) declara sus propios módulos.
El hub de cada pantalla recibe sólo los módulos del área y los filtra por permisos.
"""

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


_MODULOS_RECEPCION: tuple[AtlasModule, ...] = (
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

# Módulos del hub del médico: su jornada, su sala y su historia clínica.
_MODULOS_MEDICO: tuple[AtlasModule, ...] = (
    AtlasModule(
        id="agenda_medico",
        label="Mi agenda",
        metaphor="agenda",
        description="Citas de hoy, estados y siguiente paciente",
        asset_closed=f"{ASSET_BASE}/citas_agenda_cerrada.webp",
        asset_open=f"{ASSET_BASE}/citas_agenda_abierta.webp",
    ),
    AtlasModule(
        id="espera_medico",
        label="Sala de espera",
        metaphor="mostrador",
        description="Quién espera, cuánto lleva y si ya tiene signos",
        asset_closed=f"{ASSET_BASE}/recepcion.webp",
        asset_open=f"{ASSET_BASE}/sala_espera.webp",
    ),
    AtlasModule(
        id="historia_medico",
        label="Historia clínica",
        metaphor="archivador",
        description="Consultas cerradas y diagnósticos frecuentes",
        asset_closed=f"{ASSET_BASE}/historia_carpeta_cerrada.webp",
        asset_open=f"{ASSET_BASE}/historia_carpeta_abierta.webp",
    ),
)

# Módulos del hub del especialista: su agenda, su sala y su bandeja de derivaciones.
_MODULOS_ESPECIALISTA: tuple[AtlasModule, ...] = (
    AtlasModule(
        id="agenda_especialista",
        label="Mi agenda",
        metaphor="agenda",
        description="Citas de hoy, estados y siguiente paciente",
        asset_closed=f"{ASSET_BASE}/citas_agenda_cerrada.webp",
        asset_open=f"{ASSET_BASE}/citas_agenda_abierta.webp",
    ),
    AtlasModule(
        id="espera_especialista",
        label="Sala de espera",
        metaphor="mostrador",
        description="Quién espera, cuánto lleva y si ya tiene signos",
        asset_closed=f"{ASSET_BASE}/recepcion.webp",
        asset_open=f"{ASSET_BASE}/sala_espera.webp",
    ),
    AtlasModule(
        id="derivaciones",
        label="Derivaciones",
        metaphor="consultorio",
        description="Bandeja de referencias por prioridad y especialidad",
        asset_closed=f"{ASSET_BASE}/consultas.webp",
        asset_open=f"{ASSET_BASE}/diagnostico.webp",
    ),
)

_MAPAS_POR_AREA: dict[str, tuple[AtlasModule, ...]] = {
    "recepcion": _MODULOS_RECEPCION,
    "medico": _MODULOS_MEDICO,
    "especialista": _MODULOS_ESPECIALISTA,
}

# Módulos que exponen datos de pacientes: sin este permiso no se muestran.
_REQUIERE_PACIENTES = frozenset({"pacientes", "citas", "historia_medico", "derivaciones"})


def modules_for_hub(user, area: str = "recepcion") -> list[AtlasModule]:
    """Módulos visibles en el hub del área, ya filtrados por permisos."""
    out: list[AtlasModule] = []
    for module in _MAPAS_POR_AREA.get(area, ()):
        if module.id in _REQUIERE_PACIENTES and not can_view_pacientes(user):
            continue
        out.append(module)
    return out


def module_by_id(module_id: str, area: str | None = None) -> AtlasModule | None:
    """Busca un módulo por id; con ``area`` restringe la búsqueda a esa área."""
    areas = [area] if area else list(_MAPAS_POR_AREA)
    for name in areas:
        for module in _MAPAS_POR_AREA.get(name, ()):
            if module.id == module_id:
                return module
    return None
