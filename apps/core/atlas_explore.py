"""Datos agregados para paneles de exploración Atlas (sin PHI en gráficos)."""

from __future__ import annotations

from collections import defaultdict
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.atlas_assets import estado_cita_icon
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
    """Rutas static de avatares genéricos por prefijo de grupo (sin PHI)."""
    folder = settings.BASE_DIR / "static" / "atlas-interactive" / "assets" / "v1" / "avatares"
    if not folder.is_dir():
        return []
    paths = sorted(folder.glob(f"{group_id}_*.webp"))[:limit]
    return [f"{AVATAR_ASSET_BASE}/{p.name}" for p in paths]


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
    por_estado = []
    estado_labels = dict(Cita.ESTADO_CHOICES)
    for row in hoy_qs.values("estado").annotate(total=Count("id")).order_by("-total"):
        est = row["estado"]
        por_estado.append(
            {
                "estado": est,
                "total": row["total"],
                "label": estado_labels.get(est, est),
                "icon": estado_cita_icon(est),
            }
        )

    return {
        "hoy_total": hoy_qs.count(),
        "proximas_total": proximas.count(),
        "por_estado_hoy": por_estado,
        "fecha": hoy,
    }
