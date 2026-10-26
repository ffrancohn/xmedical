"""Franja del hilo clínico: dónde está cada persona hoy."""
from django.utils import timezone

from apps.citas.models import Cita
from apps.preclinica.models import Preclinica
from apps.referencias.models import Referencia

ESTACIONES = (
    ("agendar", "Agendar", "Aún no llegan"),
    ("recibir", "Recibir", "En sala"),
    ("medir", "Medir", "En signos"),
    ("atender", "Atender", "Listos para consulta"),
    ("derivar", "Derivar", "Hacia especialidad"),
)
ORDEN = [item[0] for item in ESTACIONES]

VISTAS = {
    "recepcion": {"open": ["agendar", "recibir"], "mine": ["agendar", "recibir"]},
    "enfermeria": {"open": ["medir"], "mine": ["medir"]},
    "medico": {"open": ["atender"], "mine": ["atender"]},
    "especialista": {"open": ["derivar"], "mine": ["derivar"]},
}


def _persona(paciente):
    nombre = f"{paciente.nombre} {paciente.apellido}".strip()
    iniciales = f"{(paciente.nombre or ' ')[:1]}{(paciente.apellido or ' ')[:1]}".upper()
    return {"iniciales": iniciales, "nombre": nombre}


def _estacion(station_id, name, caption, people, vista, line="", avatar=None, done=False):
    return {
        "id": station_id,
        "name": name,
        "caption": caption,
        "line": line,
        "count": len(people),
        "people": people[:3],
        "extra": max(len(people) - 3, 0),
        "open": station_id in vista["open"],
        "mine": station_id in vista["mine"],
        "done": done,
        "avatar": avatar,
    }


def hilo_del_dia(instituciones, rol, fecha=None):
    """Ocupación de la clínica. Cada cita activa cae en una estación; Medir repite la sala."""
    fecha = fecha or timezone.localdate()
    vista = VISTAS[rol]
    citas = list(
        Cita.objects.select_related("paciente")
        .filter(institucion__in=instituciones, fecha=fecha)
        .exclude(estado="cancelada")
        .order_by("hora", "id")
    )
    con_preclinica = set(
        Preclinica.objects.filter(cita_id__in=[cita.id for cita in citas]).values_list("cita_id", flat=True)
    )

    grupos = {"agendar": [], "recibir": [], "atender": []}
    for cita in citas:
        if cita.estado == "atendida":
            continue
        persona = _persona(cita.paciente)
        if cita.id in con_preclinica:
            grupos["atender"].append(persona)
        elif cita.estado == "en_espera":
            grupos["recibir"].append(persona)
        elif cita.estado in ("pendiente", "confirmada"):
            grupos["agendar"].append(persona)

    # Quien ya llegó y aún no tiene signos es la cola de enfermería.
    grupos["medir"] = list(grupos["recibir"])
    referencias = (
        Referencia.objects.select_related("consulta_origen__cita__paciente")
        .filter(institucion__in=instituciones, estado="pendiente")
        .order_by("-prioridad", "-creado_en")
    )
    grupos["derivar"] = [_persona(referencia.paciente) for referencia in referencias]

    stations = [
        _estacion(station_id, name, caption, grupos[station_id], vista)
        for station_id, name, caption in ESTACIONES
    ]
    return {"personal": False, "kicker": "El hilo de hoy", "stations": stations}


def hilo_paciente(paciente, institucion, fecha=None):
    """El paciente solo ve su lugar. No incluye la ocupación de los demás."""
    fecha = fecha or timezone.localdate()
    citas = Cita.objects.filter(paciente=paciente, institucion=institucion).exclude(estado="cancelada")
    cita = (
        citas.filter(fecha=fecha).order_by("hora", "id").first()
        or citas.filter(fecha__gt=fecha).exclude(estado="atendida").order_by("fecha", "hora", "id").first()
    )
    tiene_preclinica = bool(cita and Preclinica.objects.filter(cita=cita).exists())
    tiene_referencia = Referencia.objects.filter(
        institucion=institucion,
        estado="pendiente",
        consulta_origen__cita__paciente=paciente,
    ).exists()

    if cita is None:
        actual = "agendar"
        terminada = False
        lineas = {
            "agendar": "Aún no tienes una cita. Cuando la agendes, empiezas aquí.",
            "recibir": "Cuando llegues a la clínica.",
            "medir": "Enfermería toma tus signos.",
            "atender": "La consulta con tu médico.",
            "derivar": "Solo si te envían a especialidad.",
        }
    else:
        terminada = cita.estado == "atendida" and not tiene_referencia
        if cita.estado == "atendida" and tiene_referencia:
            actual = "derivar"
        elif tiene_preclinica or cita.estado == "atendida":
            actual = "atender"
        elif cita.estado == "en_espera":
            actual = "recibir"
        else:
            actual = "agendar"
        cuando = cita.fecha.strftime("%d/%m")
        hora = cita.hora.strftime("%H:%M")
        lineas = {
            "agendar": f"Tu cita del {cuando} a las {hora} ya está agendada. Siguiente: Recibir.",
            "recibir": "Estás aquí. Siguiente: Medir." if actual == "recibir" else "Llegada a la clínica.",
            "medir": "Siguiente paso, cuando pases a enfermería.",
            "atender": "Tu consulta de hoy ya terminó." if terminada else "Estás aquí. Siguiente: la consulta.",
            "derivar": "Te enviaron a especialidad." if actual == "derivar" else "Solo si te envían a especialidad.",
        }

    idx = ORDEN.index(actual)
    hechos = set(ORDEN[:idx])
    if terminada:
        hechos.add("atender")
    avatar = _persona(paciente)
    vista = {"open": [actual], "mine": [actual]}
    stations = []
    for station_id, name, caption in ESTACIONES:
        stations.append(
            _estacion(
                station_id,
                name,
                caption,
                [],
                vista,
                line=lineas[station_id],
                avatar=avatar if station_id == actual else None,
                done=station_id in hechos,
            )
        )
    return {"personal": True, "kicker": "Tu lugar en el hilo", "stations": stations}
