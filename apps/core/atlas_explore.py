"""Datos agregados para paneles de exploración Atlas (sin PHI en gráficos)."""

from __future__ import annotations

from collections import defaultdict
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion
from django.conf import settings

from apps.pacientes.models import Paciente

AVATAR_ASSET_BASE = "atlas-interactive/assets/v1/avatares"

# Rangos por defecto; override en institucion.configuracion["pacientes_grupos_edad"]
DEFAULT_AGE_BUCKETS: tuple[dict, ...] = (
    {"id": "ninos", "label": "Niños", "min_years": 0, "max_years": 11},
    {"id": "adolescentes", "label": "Adolescentes", "min_years": 12, "max_years": 17},
    {"id": "adultos_jovenes", "label": "Adultos jóvenes", "min_years": 18, "max_years": 29},
    {"id": "adultos", "label": "Adultos", "min_years": 30, "max_years": 59},
    {"id": "mayores", "label": "Personas mayores", "min_years": 60, "max_years": 150},
)


def get_age_buckets(institucion: Institucion | None) -> list[dict]:
    cfg = {}
    if institucion and isinstance(institucion.configuracion, dict):
        cfg = institucion.configuracion.get("pacientes_grupos_edad") or {}
    if cfg.get("buckets"):
        return list(cfg["buckets"])
    return [dict(b) for b in DEFAULT_AGE_BUCKETS]


def _age_years(fecha_nac, on_date=None) -> int | None:
    if not fecha_nac:
        return None
    on_date = on_date or timezone.localdate()
    delta = relativedelta(on_date, fecha_nac)
    return delta.years


def _bucket_for_age(age: int | None, buckets: list[dict]) -> str:
    if age is None:
        return "sin_edad"
    for b in buckets:
        if b["min_years"] <= age <= b["max_years"]:
            return b["id"]
    return "sin_edad"


def birth_date_range_for_bucket(bucket_id: str, buckets: list[dict], on_date=None):
    """Límites de fecha_nacimiento para filtrar un bucket en queryset."""
    on_date = on_date or timezone.localdate()
    for b in buckets:
        if b["id"] != bucket_id:
            continue
        latest_birth = on_date - relativedelta(years=b["min_years"])
        earliest_birth = on_date - relativedelta(years=b["max_years"] + 1, days=+1)
        return earliest_birth, latest_birth
    return None, None


def avatar_static_paths(group_id: str, limit: int = 4) -> list[str]:
    """Rutas static de avatares genéricos del grupo (sin PHI).

    Acepta el paquete v1 (`ninos_01.webp`) y el v2 (`ninos_masculino.webp`).
    El filtro es por nombre completo del grupo: `adultos_*` no debe capturar
    `adultos_jovenes_*`.
    """
    import re

    folder = settings.BASE_DIR / "static" / "atlas-interactive" / "assets" / "v1" / "avatares"
    if not folder.is_dir():
        return []
    patron = re.compile(rf"^{re.escape(group_id)}_(masculino|femenino|\d+)\.webp$")
    nombres = sorted(p.name for p in folder.iterdir() if p.is_file() and patron.match(p.name))
    return [f"{AVATAR_ASSET_BASE}/{nombre}" for nombre in nombres[:limit]]


def pacientes_exploracion(instituciones, institucion_principal=None) -> dict:
    """Conteos por grupo de edad; avatares son índices genéricos, no pacientes reales."""
    buckets = get_age_buckets(institucion_principal or (instituciones[0] if instituciones else None))
    qs = Paciente.objects.filter(activo=True, institucion__in=instituciones).only(
        "fecha_nacimiento", "sexo"
    )

    counts: dict[str, int] = defaultdict(int)
    sexo_por_grupo: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    sin_edad = 0

    for p in qs.iterator():
        age = _age_years(p.fecha_nacimiento)
        bid = _bucket_for_age(age, buckets)
        if bid == "sin_edad":
            sin_edad += 1
            continue
        counts[bid] += 1
        if p.sexo:
            sexo_por_grupo[bid][p.sexo] += 1

    grupos = []
    for b in buckets:
        avatars = avatar_static_paths(b["id"], limit=4)
        grupos.append(
            {
                "id": b["id"],
                "label": b["label"],
                "count": counts.get(b["id"], 0),
                "avatar_paths": avatars,
                "avatar_variants": len(avatars) or min(4, max(1, counts.get(b["id"], 0))),
                "sexo": dict(sexo_por_grupo.get(b["id"], {})),
            }
        )

    return {
        "buckets": buckets,
        "grupos": grupos,
        "sin_edad": sin_edad,
        "total": qs.count(),
    }


def citas_exploracion(instituciones) -> dict:
    hoy = timezone.localdate()
    base = Cita.objects.filter(institucion__in=instituciones).exclude(estado="cancelada")
    hoy_qs = base.filter(fecha=hoy)
    proximas = base.filter(fecha__gt=hoy, fecha__lte=hoy + timedelta(days=14))
    por_estado = list(hoy_qs.values("estado").annotate(total=Count("id")).order_by("-total"))

    return {
        "hoy_total": hoy_qs.count(),
        "proximas_total": proximas.count(),
        "por_estado_hoy": por_estado,
        "fecha": hoy,
    }


# ---------------------------------------------------------------------------
# Hub del médico: su jornada, su sala de espera y su historia clínica.
# Todos los agregados son conteos o tiempos: no se exponen nombres de pacientes
# (la tabla de la agenda sigue siendo la vista primaria para eso).
# ---------------------------------------------------------------------------


def _citas_del_medico(instituciones, profesional, fecha):
    qs = Cita.objects.filter(institucion__in=instituciones, fecha=fecha)
    if profesional is not None:
        qs = qs.filter(profesional=profesional)
    return qs


def agenda_exploracion(instituciones, profesional=None) -> dict:
    """Citas de hoy por estado y la siguiente pendiente de atender (médico y especialista)."""
    hoy = timezone.localdate()
    base = _citas_del_medico(instituciones, profesional, hoy).exclude(estado="cancelada")

    por_estado = []
    for code, label in Cita.ESTADO_CHOICES:
        if code == "cancelada":
            continue
        por_estado.append(
            {
                "code": code,
                "label": label,
                "total": base.filter(estado=code).count(),
            }
        )

    tope = max((fila["total"] for fila in por_estado), default=0)
    for fila in por_estado:
        fila["pct"] = round(fila["total"] * 100 / tope) if tope else 0

    ahora = timezone.localtime()
    pendientes = base.filter(
        estado__in=("pendiente", "confirmada", "en_espera"),
        hora__gte=ahora.time(),
    ).order_by("hora")
    proxima = pendientes.first()

    return {
        "hoy_total": base.count(),
        "atendidas": base.filter(estado="atendida").count(),
        "por_estado": por_estado,
        "por_atender": pendientes.count(),
        "proxima_hora": proxima.hora if proxima else None,
        "fecha": hoy,
    }


def espera_exploracion(instituciones, profesional=None) -> dict:
    """Presión de la sala: cuántos esperan, quiénes ya tienen signos y hace cuánto (médico y especialista)."""
    from apps.preclinica.models import Preclinica

    hoy = timezone.localdate()
    ahora = timezone.localtime()
    base = _citas_del_medico(instituciones, profesional, hoy).filter(
        estado__in=("pendiente", "confirmada", "en_espera")
    )

    citas = list(base.order_by("hora"))
    con_signos = (
        set(Preclinica.objects.filter(cita_id__in=[c.id for c in citas]).values_list("cita_id", flat=True))
        if citas
        else set()
    )

    en_curso = ahora.hour * 60 + ahora.minute
    esperas = []
    for cita in citas:
        inicio = cita.hora.hour * 60 + cita.hora.minute
        esperas.append(max(en_curso - inicio, 0))

    return {
        "en_espera": len(citas),
        "listos": sum(1 for c in citas if c.id in con_signos),
        "sin_signos": sum(1 for c in citas if c.id not in con_signos),
        "espera_media": round(sum(esperas) / len(esperas)) if esperas else 0,
        "espera_maxima": max(esperas, default=0),
        "tope_espera": 30,
    }


def historia_medico_exploracion(instituciones, profesional=None) -> dict:
    """Volumen asistencial y diagnósticos más frecuentes de los últimos 30 días."""
    from apps.consulta.models import Consulta, Diagnostico

    hoy = timezone.localdate()
    desde = hoy - timedelta(days=30)

    consultas = Consulta.objects.filter(
        institucion__in=instituciones, cita__fecha__gte=desde, cita__fecha__lte=hoy
    )
    diagnosticos = Diagnostico.objects.filter(
        institucion__in=instituciones, consulta__cita__fecha__gte=desde, consulta__cita__fecha__lte=hoy
    )
    if profesional is not None:
        consultas = consultas.filter(cita__profesional=profesional)
        diagnosticos = diagnosticos.filter(consulta__cita__profesional=profesional)

    top = list(
        diagnosticos.values("nombre")
        .annotate(total=Count("id"))
        .order_by("-total", "nombre")[:5]
    )
    tope = top[0]["total"] if top else 0
    for fila in top:
        fila["pct"] = round(fila["total"] * 100 / tope) if tope else 0

    return {
        "consultas_30d": consultas.count(),
        "consultas_hoy": consultas.filter(cita__fecha=hoy).count(),
        "top_diagnosticos": top,
        "total_diagnosticos": diagnosticos.count(),
        "desde": desde,
    }


def referencias_exploracion(instituciones, profesional=None) -> dict:
    """Bandeja de derivaciones del especialista: volumen, prioridad y antigüedad."""
    from django.db.models import Avg, DurationField, ExpressionWrapper, F
    from django.db.models.functions import Now

    from apps.referencias.models import Referencia

    base = Referencia.objects.filter(institucion__in=instituciones)
    if profesional is not None:
        if getattr(profesional, "especialidad_id", None):
            base = base.filter(
                Q(estado="pendiente", especialidad_destino=profesional.especialidad)
                | Q(especialista=profesional)
                | Q(medico_referente=profesional)
            )
        else:
            base = base.filter(Q(especialista=profesional) | Q(medico_referente=profesional))

    pendientes = base.filter(estado="pendiente")

    por_prioridad = []
    for code, label in Referencia.PRIORIDAD_CHOICES:
        por_prioridad.append(
            {"code": code, "label": label, "total": pendientes.filter(prioridad=code).count()}
        )
    tope = max((fila["total"] for fila in por_prioridad), default=0)
    for fila in por_prioridad:
        fila["pct"] = round(fila["total"] * 100 / tope) if tope else 0

    por_especialidad = list(
        pendientes.values("especialidad_destino__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:4]
    )

    espera = pendientes.aggregate(
        media=Avg(ExpressionWrapper(Now() - F("creado_en"), output_field=DurationField()))
    )["media"]

    return {
        "pendientes": pendientes.count(),
        "aceptadas": base.filter(estado="aceptada").count(),
        "completadas": base.filter(estado="completada").count(),
        "por_prioridad": por_prioridad,
        "por_especialidad": por_especialidad,
        "espera_media_dias": round(espera.total_seconds() / 86400, 1) if espera else 0,
    }
