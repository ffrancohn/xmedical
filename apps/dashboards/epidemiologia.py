from collections import defaultdict
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.consulta.models import Diagnostico


def get_epidemiologia_config(institucion):
    defaults = {
        "umbral_brote": 5,
        "ventana_dias": 7,
        "meses_tendencia": 6,
    }
    if not institucion:
        return defaults
    cfg = (
        institucion.configuracion.get("epidemiologia", {})
        if isinstance(institucion.configuracion, dict)
        else {}
    )
    return {**defaults, **cfg}


def _config_efectiva(instituciones):
    configs = [get_epidemiologia_config(inst) for inst in instituciones]
    return {
        "umbral_brote": max(c["umbral_brote"] for c in configs),
        "ventana_dias": max(c["ventana_dias"] for c in configs),
        "meses_tendencia": max(c["meses_tendencia"] for c in configs),
    }


def detectar_alertas_brote(instituciones, fecha=None):
    fecha = fecha or timezone.localdate()
    config = _config_efectiva(instituciones)
    desde = fecha - timedelta(days=config["ventana_dias"] - 1)

    diagnosticos = (
        Diagnostico.objects.filter(
            institucion__in=instituciones,
            consulta__creado_en__date__gte=desde,
            consulta__creado_en__date__lte=fecha,
        )
        .values("codigo_cie10", "nombre", "institucion_id")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    alertas = []
    for item in diagnosticos:
        if item["total"] >= config["umbral_brote"]:
            alertas.append(
                {
                    "codigo_cie10": item["codigo_cie10"],
                    "nombre": item["nombre"],
                    "total": item["total"],
                    "institucion_id": item["institucion_id"],
                    "ventana_dias": config["ventana_dias"],
                    "desde": desde,
                    "hasta": fecha,
                }
            )
    return alertas


def tendencias_diagnosticos(instituciones, meses=None):
    fecha = timezone.localdate()
    config = _config_efectiva(instituciones)
    meses = meses or config["meses_tendencia"]
    desde = fecha.replace(day=1) - timedelta(days=30 * (meses - 1))

    qs = (
        Diagnostico.objects.filter(
            institucion__in=instituciones,
            consulta__creado_en__date__gte=desde,
        )
        .annotate(mes=TruncMonth("consulta__creado_en"))
        .values("mes", "codigo_cie10", "nombre")
        .annotate(total=Count("id"))
        .order_by("mes", "-total")
    )

    por_codigo = defaultdict(lambda: {"nombre": "", "meses": defaultdict(int), "total": 0})
    meses_set = set()
    for row in qs:
        codigo = row["codigo_cie10"]
        mes_key = row["mes"].strftime("%Y-%m")
        meses_set.add(mes_key)
        por_codigo[codigo]["nombre"] = row["nombre"]
        por_codigo[codigo]["meses"][mes_key] += row["total"]
        por_codigo[codigo]["total"] += row["total"]

    meses_ordenados = sorted(meses_set)
    top = sorted(por_codigo.items(), key=lambda item: item[1]["total"], reverse=True)[:8]

    series = []
    max_valor = 1
    for codigo, data in top:
        puntos = [data["meses"].get(mes, 0) for mes in meses_ordenados]
        max_valor = max(max_valor, max(puntos) if puntos else 1)
        series.append(
            {
                "codigo_cie10": codigo,
                "nombre": data["nombre"],
                "puntos": puntos,
                "total": data["total"],
            }
        )

    return {
        "meses": meses_ordenados,
        "series": series,
        "max_valor": max_valor,
    }


def resumen_diagnosticos_periodo(instituciones, dias=30):
    desde = timezone.localdate() - timedelta(days=dias - 1)
    return list(
        Diagnostico.objects.filter(
            institucion__in=instituciones,
            consulta__creado_en__date__gte=desde,
        )
        .values("codigo_cie10", "nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )


CHART_COLORS = (
    "#2563eb",
    "#0891b2",
    "#059669",
    "#d97706",
    "#dc2626",
    "#7c3aed",
    "#db2777",
    "#4b5563",
)


def tendencias_chart_geometry(tendencias, width=520, height=220):
    """Coordenadas SVG para líneas de tendencia (sin JS)."""
    meses = tendencias.get("meses") or []
    series = tendencias.get("series") or []
    if not meses or not series:
        return None

    n = len(meses)
    max_v = max(int(tendencias.get("max_valor") or 1), 1)
    pad_l, pad_r, pad_t, pad_b = 40, 16, 18, 32
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    def x_at(i):
        if n == 1:
            return pad_l + plot_w / 2
        return pad_l + (i / (n - 1)) * plot_w

    def y_at(value):
        return pad_t + plot_h - (value / max_v) * plot_h

    series_out = []
    for idx, serie in enumerate(series):
        puntos = serie.get("puntos") or []
        coords = [(x_at(i), y_at(v)) for i, v in enumerate(puntos)]
        series_out.append(
            {
                "codigo_cie10": serie["codigo_cie10"],
                "nombre": serie["nombre"],
                "color": CHART_COLORS[idx % len(CHART_COLORS)],
                "polyline": " ".join(f"{cx:.1f},{cy:.1f}" for cx, cy in coords),
                "dots": [{"cx": cx, "cy": cy} for cx, cy in coords],
            }
        )

    x_labels = [{"x": x_at(i), "label": f"{mes[5:7]}/{mes[2:4]}"} for i, mes in enumerate(meses)]
    y_ticks = sorted({0, max_v // 2, max_v} if max_v > 1 else {0, max_v})

    return {
        "width": width,
        "height": height,
        "pad_l": pad_l,
        "pad_r": pad_r,
        "pad_t": pad_t,
        "plot_h": plot_h,
        "x2": width - pad_r,
        "series": series_out,
        "x_labels": x_labels,
        "y_ticks": [{"y": y_at(v), "label": v} for v in y_ticks],
        "baseline_y": pad_t + plot_h,
    }


def epidemiologia_dashboard_data(instituciones, fecha=None):
    fecha = fecha or timezone.localdate()
    config = _config_efectiva(instituciones)
    brotes = detectar_alertas_brote(instituciones, fecha=fecha)
    tendencias = tendencias_diagnosticos(instituciones, meses=config["meses_tendencia"])
    top_mes = resumen_diagnosticos_periodo(instituciones, dias=30)
    max_top = top_mes[0]["total"] if top_mes else 1

    return {
        "fecha": fecha,
        "config": config,
        "alertas_brote": brotes,
        "total_brotes": len(brotes),
        "tendencias": tendencias,
        "tendencias_chart": tendencias_chart_geometry(tendencias),
        "top_diagnosticos_mes": top_mes,
        "top_diagnosticos_max": max_top,
        "total_diagnosticos_mes": sum(item["total"] for item in top_mes),
    }
