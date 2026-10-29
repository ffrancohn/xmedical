"""Estado del plano de la clínica: qué pasa en cada sala ahora mismo.

Todo se deriva de lo que el personal ya registra (`Cita.estado`, `Preclinica`), sin
sensores: una sala está «esperando» si su cita está en ese estado, «reservado» si la
cita aún no llega, «atendida» si ya cerró y «libre» si no tiene nada.
"""

from __future__ import annotations

from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Espacio
from apps.preclinica.models import Preclinica

UMBRAL_ESPERA_MIN = 20

ESTADOS = {
    "libre": {"etiqueta": "Libre", "tono": "libre"},
    "reservado": {"etiqueta": "Reservado", "tono": "reservado"},
    "esperando": {"etiqueta": "Esperando", "tono": "esperando"},
    "atendida": {"etiqueta": "Atendida", "tono": "atendida"},
}


def _minutos(desde, hasta) -> int:
    delta = (hasta - desde).total_seconds() / 60
    return int(delta)


def _cita_actual(citas: list[Cita]):
    """Prioridad: en espera > próxima reservada > última atendida."""
    en_espera = next((c for c in citas if c.estado == "en_espera"), None)
    if en_espera:
        return en_espera, "esperando"
    reservada = next((c for c in citas if c.estado in ("pendiente", "confirmada")), None)
    if reservada:
        return reservada, "reservado"
    atendida = next((c for c in reversed(citas) if c.estado == "atendida"), None)
    if atendida:
        return atendida, "atendida"
    return None, "libre"


def estado_plano(instituciones, fecha=None) -> dict:
    fecha = fecha or timezone.localdate()
    ahora = timezone.localtime()

    espacios = list(
        Espacio.objects.filter(institucion__in=instituciones, activo=True)
        .select_related("especialidad")
        .order_by("planta", "y", "x")
    )
    citas = list(
        Cita.objects.filter(institucion__in=instituciones, fecha=fecha)
        .exclude(estado="cancelada")
        .select_related("paciente", "profesional")
        .order_by("hora")
    )
    con_signos = set(
        Preclinica.objects.filter(cita__in=citas).values_list("cita_id", flat=True)
    )

    por_espacio: dict[int, list[Cita]] = {}
    sin_sala = 0
    for cita in citas:
        if cita.espacio_id:
            por_espacio.setdefault(cita.espacio_id, []).append(cita)
        else:
            sin_sala += 1

    filas = []
    esperas = []
    for espacio in espacios:
        lista = por_espacio.get(espacio.id, [])
        cita, estado = _cita_actual(lista)

        minutos = None
        iniciales = ""
        if cita is not None:
            hora_cita = timezone.make_aware(
                timezone.datetime.combine(cita.fecha, cita.hora), timezone.get_current_timezone()
            )
            minutos = _minutos(hora_cita, ahora)
            iniciales = f"{cita.paciente.nombre[:1]}{cita.paciente.apellido[:1]}".upper()
            if estado == "esperando":
                esperas.append(max(minutos, 0))

        critico = estado == "esperando" and (minutos or 0) >= UMBRAL_ESPERA_MIN
        atrasada = estado == "reservado" and (minutos or 0) > 5
        filas.append(
            {
                "id": espacio.id,
                "nombre": espacio.nombre,
                "tipo": espacio.get_tipo_display(),
                "mostrar_tipo": espacio.get_tipo_display().lower() != espacio.nombre.lower(),
                "especialidad": espacio.especialidad.nombre if espacio.especialidad else "",
                "estado": estado,
                "estado_etiqueta": ESTADOS[estado]["etiqueta"],
                "tono": "critico" if critico else ESTADOS[estado]["tono"],
                "critico": critico,
                "atrasada": atrasada,
                "iniciales": iniciales,
                "minutos": minutos if estado in ("esperando", "atendida") or atrasada else None,
                "minutos_para": -minutos if estado == "reservado" and minutos is not None and not atrasada else None,
                "con_signos": bool(cita and cita.id in con_signos),
                "profesional": cita.profesional.nombre if cita and cita.profesional else "",
                "x": espacio.x,
                "y": espacio.y,
                "ancho": espacio.ancho,
                "alto": espacio.alto,
                "planta": espacio.planta,
                "capacidad": espacio.capacidad,
            }
        )

    columnas = max([f["x"] + f["ancho"] for f in filas] + [8])
    filas_plano = max([f["y"] + f["alto"] for f in filas] + [6])

    return {
        "fecha": fecha,
        "hora": ahora.strftime("%H:%M"),
        "espacios": filas,
        "por_espera": sorted(
            [f for f in filas if f["estado"] == "esperando"],
            key=lambda f: f["minutos"] or 0,
            reverse=True,
        ),
        "columnas": columnas,
        "filas": filas_plano,
        "total": len(filas),
        "libres": sum(1 for f in filas if f["estado"] == "libre"),
        "esperando": sum(1 for f in filas if f["estado"] == "esperando"),
        "criticos": sum(1 for f in filas if f["critico"]),
        "sin_sala": sin_sala,
        "espera_media": round(sum(esperas) / len(esperas)) if esperas else 0,
        "espera_maxima": max(esperas) if esperas else 0,
    }
