"""Sinónimos y abreviaturas frecuentes en consulta (español, Honduras).

El catálogo CIE-10 usa el nombre oficial; el médico escribe abreviaturas. Esta
tabla traduce lo que se teclea a un término que sí aparece en el catálogo.
Las claves van normalizadas (sin tildes, minúsculas).
"""

from __future__ import annotations

from apps.consulta.models import normalizar_texto

SINONIMOS: dict[str, str] = {
    "hta": "hipertension",
    "hipertension arterial": "hipertension",
    "dm": "diabetes mellitus",
    "dm1": "diabetes mellitus insulinodependiente",
    "dm2": "diabetes mellitus no insulinodependiente",
    "diabetes tipo 2": "diabetes mellitus no insulinodependiente",
    "diabetes tipo 1": "diabetes mellitus insulinodependiente",
    "epoc": "enfermedad pulmonar obstructiva cronica",
    "iam": "infarto agudo de miocardio",
    "acv": "infarto cerebral",
    "ekg": "electrocardiograma",
    "itu": "infeccion de vias urinarias",
    "iviu": "infeccion de vias urinarias",
    "erc": "enfermedad renal cronica",
    "irc": "insuficiencia renal cronica",
    "ira": "insuficiencia renal aguda",
    "tb": "tuberculosis",
    "vih": "virus de la inmunodeficiencia humana",
    "sida": "virus de la inmunodeficiencia humana",
    "hpylori": "helicobacter pylori",
    "sx": "sindrome",
    "ca": "neoplasma",
    "evc": "infarto cerebral",
    "fa": "fibrilacion auricular",
    "icc": "insuficiencia cardiaca",
}


def expandir_termino(valor: str) -> list[str]:
    """Término normalizado + su expansión si es una abreviatura conocida."""
    termino = normalizar_texto(valor)
    if not termino:
        return []
    expandido = SINONIMOS.get(termino)
    if expandido and expandido != termino:
        return [termino, expandido]
    return [termino]
