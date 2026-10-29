"""Payload de la escena isométrica del consultorio (modo Atlas).

Convierte los agregados de `atlas_explore` en estaciones con KPIs, barras y
acciones listas para pintar. Funciones puras: reciben los diccionarios ya
calculados y devuelven dict serializable (lo consume `atlas-scene.js`).
"""

from __future__ import annotations

from django.utils import timezone

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def _hora(valor) -> str:
    return valor.strftime("%H:%M") if valor else "—"


def _barras(filas, tope: int | None = None) -> list[dict]:
    tope = tope or max((f[1] for f in filas), default=1) or 1
    return [
        {"etiqueta": f[0], "valor": f[1], "pct": round(f[1] * 100 / tope) if tope else 0}
        for f in filas
    ]


def _fecha_larga(momento) -> str:
    texto = f"{DIAS[momento.weekday()]} {momento.day} de {MESES[momento.month - 1]}, {momento:%H:%M}"
    return texto[0].upper() + texto[1:]


def _paciente(espera: dict) -> dict:
    """El paciente sentado no tiene panel propio: enriquece la silla."""
    return {
        "ocupada": espera["en_espera"] > 0,
        "total": espera["en_espera"],
        "espera": espera["espera_maxima"],
        "con_signos": espera["listos"] > 0,
    }


def _estacion_agenda(agenda: dict, urls: dict) -> dict:
    return {
        "id": "agenda",
        "etiqueta": "Agenda de hoy",
        "kicker": "Escritorio",
        "lead": "Tus citas del día y el siguiente paciente por atender.",
        "aria": f"Agenda de hoy: {agenda['hoy_total']} citas, {agenda['atendidas']} atendidas",
        "kpis": [
            {"etiqueta": "Citas", "valor": agenda["hoy_total"]},
            {"etiqueta": "Atendidas", "valor": agenda["atendidas"]},
            {"etiqueta": "Por atender", "valor": agenda["por_atender"]},
            {"etiqueta": "Siguiente", "valor": _hora(agenda.get("proxima_hora"))},
        ],
        "barras": _barras([(f["label"], f["total"]) for f in agenda["por_estado"]]),
        "acciones": [
            {"texto": "Atender la cola de hoy", "url": urls.get("citas", "")},
            {"texto": "Agenda completa", "url": urls.get("citas", "")},
        ],
    }


def _estacion_espera(espera: dict, urls: dict) -> dict:
    return {
        "id": "espera",
        "etiqueta": "Sala de espera",
        "kicker": "Fondo de la clínica",
        "lead": "Quién espera, cuánto lleva y si ya tiene signos tomados.",
        "aria": f"Sala de espera: {espera['en_espera']} pacientes, el primero hace {espera['espera_maxima']} minutos",
        "kpis": [
            {"etiqueta": "En espera", "valor": espera["en_espera"]},
            {"etiqueta": "Con signos", "valor": espera["listos"]},
            {"etiqueta": "Sin signos", "valor": espera["sin_signos"]},
            {"etiqueta": "Mayor espera", "valor": f"{espera['espera_maxima']} min"},
        ],
        "barras": _barras(
            [("Sin signos", espera["sin_signos"]), ("Listos", espera["listos"])],
            tope=max(espera["en_espera"], 1),
        ),
        "acciones": [
            {"texto": "Ver cola de signos", "url": urls.get("preclinica", "")},
            {"texto": "Ver pacientes del día", "url": urls.get("citas", "")},
        ],
    }


def _estacion_historia(historia: dict, urls: dict) -> dict:
    top = historia["top_diagnosticos"]
    return {
        "id": "historia",
        "etiqueta": "Archivo de historias",
        "kicker": "Archivador",
        "lead": "Consultas cerradas y diagnósticos frecuentes de los últimos 30 días.",
        "aria": f"Archivo de historias: {historia['consultas_hoy']} consultas hoy",
        "kpis": [
            {"etiqueta": "Consultas hoy", "valor": historia["consultas_hoy"]},
            {"etiqueta": "30 días", "valor": historia["consultas_30d"]},
            {"etiqueta": "Diagnósticos", "valor": historia["total_diagnosticos"]},
            {"etiqueta": "Top", "valor": top[0]["nombre"][:18] if top else "—"},
        ],
        "barras": _barras([(d["nombre"][:24], d["total"]) for d in top]),
        "acciones": [
            {"texto": "Buscar paciente", "url": urls.get("pacientes", "")},
            {"texto": "Ver epidemiología", "url": urls.get("epidemiologia", "")},
        ],
    }


def _estacion_derivaciones(referencias: dict, urls: dict) -> dict:
    dias = referencias["espera_media_dias"]
    espera_txt = "menos de 1 d" if 0 <= dias < 0.1 else f"{dias} d"
    return {
        "id": "derivaciones",
        "etiqueta": "Derivaciones",
        "kicker": "Bandeja de referencias",
        "lead": "Referencias pendientes por prioridad y cuánto llevan esperando.",
        "aria": f"Derivaciones: {referencias['pendientes']} pendientes, espera media {espera_txt}",
        "kpis": [
            {"etiqueta": "Pendientes", "valor": referencias["pendientes"]},
            {"etiqueta": "Aceptadas", "valor": referencias["aceptadas"]},
            {"etiqueta": "Completadas", "valor": referencias["completadas"]},
            {"etiqueta": "Espera media", "valor": espera_txt},
        ],
        "barras": _barras(
            [(f["label"], f["total"]) for f in referencias["por_prioridad"]],
            tope=max((f["total"] for f in referencias["por_prioridad"]), default=1) or 1,
        ),
        "acciones": [
            {"texto": "Revisar bandeja", "url": urls.get("referencias", "")},
            {"texto": "Mi agenda", "url": urls.get("citas", "")},
        ],
    }


def _payload(estaciones, espera, urls, perfil, especialidad, fecha) -> dict:
    return {
        "perfil": perfil,
        "especialidad": especialidad,
        "fecha": _fecha_larga(fecha),
        "fecha_corta": fecha.strftime("%d/%m/%Y %H:%M"),
        "estaciones": estaciones,
        "paciente": _paciente(espera),
        "urls": urls,
    }


def construir_escena_medico(
    agenda: dict,
    espera: dict,
    historia: dict,
    urls: dict,
    perfil: str = "",
    especialidad: str = "",
    fecha=None,
) -> dict:
    """Escena del consultorio para el médico de primer nivel."""
    fecha = fecha or timezone.localtime()
    estaciones = [
        _estacion_agenda(agenda, urls),
        _estacion_espera(espera, urls),
        _estacion_historia(historia, urls),
    ]
    return _payload(estaciones, espera, urls, perfil, especialidad, fecha)


def construir_escena_especialista(
    agenda: dict,
    espera: dict,
    referencias: dict,
    urls: dict,
    perfil: str = "",
    especialidad: str = "",
    fecha=None,
) -> dict:
    """Escena del consultorio para el especialista: la bandeja sustituye al archivo."""
    fecha = fecha or timezone.localtime()
    estaciones = [
        _estacion_agenda(agenda, urls),
        _estacion_espera(espera, urls),
        _estacion_derivaciones(referencias, urls),
    ]
    return _payload(estaciones, espera, urls, perfil, especialidad, fecha)
