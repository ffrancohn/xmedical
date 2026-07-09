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
        "top_diagnosticos_mes": top_mes,
        "top_diagnosticos_max": max_top,
        "total_diagnosticos_mes": sum(item["total"] for item in top_mes),
    }
