"""Payload de la escena isométrica del consultorio (modo Atlas).

Convierte los agregados de `atlas_explore` en estaciones con KPIs, barras y
acciones listas para pintar. Función pura: recibe los diccionarios ya calculados
y devuelve dict serializable (lo consume `atlas-scene.js` vía json_script).
"""

from __future__ import annotations

from django.utils import timezone


def _hora(valor) -> str:
    return valor.strftime("%H:%M") if valor else "—"


def _barras(filas, tope: int | None = None) -> list[dict]:
    tope = tope or max((f[1] for f in filas), default=1) or 1
    return [
        {"etiqueta": f[0], "valor": f[1], "pct": round(f[1] * 100 / tope) if tope else 0}
        for f in filas
    ]


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
        {
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
        },
        {
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
                [
                    ("Sin signos", espera["sin_signos"]),
                    ("Listos", espera["listos"]),
                ],
                tope=max(espera["en_espera"], 1),
            ),
            "acciones": [
                {"texto": "Ver cola de signos", "url": urls.get("preclinica", "")},
                {"texto": "Ver pacientes del día", "url": urls.get("citas", "")},
            ],
        },
        {
            "id": "historia",
            "etiqueta": "Archivo de historias",
            "kicker": "Archivador",
            "lead": "Consultas cerradas y diagnósticos frecuentes de los últimos 30 días.",
            "aria": f"Archivo de historias: {historia['consultas_hoy']} consultas hoy",
            "kpis": [
                {"etiqueta": "Consultas hoy", "valor": historia["consultas_hoy"]},
                {"etiqueta": "30 días", "valor": historia["consultas_30d"]},
                {"etiqueta": "Diagnósticos", "valor": historia["total_diagnosticos"]},
                {"etiqueta": "Top", "valor": (historia["top_diagnosticos"][0]["nombre"][:18] if historia["top_diagnosticos"] else "—")},
            ],
            "barras": _barras([(d["nombre"][:24], d["total"]) for d in historia["top_diagnosticos"]]),
            "acciones": [
                {"texto": "Buscar paciente", "url": urls.get("pacientes", "")},
                {"texto": "Ver epidemiología", "url": urls.get("epidemiologia", "")},
            ],
        },
    ]

    # El paciente sentado no tiene panel propio: enriquece la silla.
    paciente = {
        "ocupada": espera["en_espera"] > 0,
        "total": espera["en_espera"],
        "espera": espera["espera_maxima"],
        "con_signos": espera["listos"] > 0,
    }

    return {
        "perfil": perfil,
        "especialidad": especialidad,
        "fecha": fecha.strftime("%A %d de %B, %H:%M").capitalize(),
        "estaciones": estaciones,
        "paciente": paciente,
        "urls": urls,
    }
