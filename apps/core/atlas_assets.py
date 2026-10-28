"""Rutas static de iconos Atlas v1."""

ESTADO_CITA_ICON: dict[str, str] = {
    "confirmada": "atlas-interactive/assets/v1/estados/confirmada.webp",
    "en_espera": "atlas-interactive/assets/v1/estados/en_espera.webp",
    "cancelada": "atlas-interactive/assets/v1/estados/cancelada.webp",
    "atendida": "atlas-interactive/assets/v1/estados/finalizada.webp",
    "pendiente": "atlas-interactive/assets/v1/estados/en_espera.webp",
}


def estado_cita_icon(estado: str) -> str | None:
    return ESTADO_CITA_ICON.get(estado)
