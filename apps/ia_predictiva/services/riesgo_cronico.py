from decimal import Decimal

from apps.preclinica.models import Preclinica

from ..config import get_predictiva_config
from ..models import AlertaRiesgoCronico

DIABETES_KEYWORDS = ("diabetes", "diabet", "glucosa", "azucar en sangre")
HTA_KEYWORDS = ("hipertension", "hta", "presion alta", "tension alta")


def _texto_riesgo_familiar(paciente):
    texto = " ".join(
        filter(
            None,
            [
                paciente.observaciones or "",
                paciente.contacto_emergencia_nombre or "",
            ],
        )
    ).lower()
    return texto


def _ultimas_preclinicas(paciente, institucion, limite=5):
    return (
        Preclinica.objects.select_related("cita")
        .filter(cita__paciente=paciente, institucion=institucion)
        .order_by("-creado_en")[:limite]
    )


def _imc_reciente(paciente, institucion, preclinica=None):
    if preclinica and preclinica.imc:
        return preclinica.imc
    ultima = (
        Preclinica.objects.filter(cita__paciente=paciente, institucion=institucion, imc__isnull=False)
        .order_by("-creado_en")
        .first()
    )
    return ultima.imc if ultima else None


def evaluar_riesgo_diabetes(paciente, institucion, preclinica=None):
    imc = _imc_reciente(paciente, institucion, preclinica)
    texto = _texto_riesgo_familiar(paciente)
    antecedente = any(k in texto for k in DIABETES_KEYWORDS)

    nivel = None
    mensaje = None
    if imc and imc >= Decimal("30"):
        nivel = "alto"
        mensaje = "Riesgo alto de diabetes - considerar screening (IMC elevado)"
    elif imc and imc >= Decimal("25"):
        nivel = "medio"
        mensaje = "Riesgo medio de diabetes - vigilar factores metabolicos"
    elif antecedente:
        nivel = "medio"
        mensaje = "Riesgo medio de diabetes - antecedentes familiares reportados"

    if antecedente and nivel == "alto":
        mensaje = "Riesgo alto de diabetes - IMC elevado y antecedentes familiares"

    if nivel:
        return {"tipo": "diabetes", "nivel": nivel, "mensaje": mensaje}
    return None


def evaluar_riesgo_hta(paciente, institucion, preclinica=None):
    preclinicas = list(_ultimas_preclinicas(paciente, institucion, limite=3))
    if preclinica and all(p.id != preclinica.id for p in preclinicas):
        preclinicas = [preclinica] + preclinicas[:2]

    elevadas = 0
    for registro in preclinicas:
        if registro.presion_arterial_sis and registro.presion_arterial_sis >= 140:
            elevadas += 1
        elif registro.presion_arterial_dia and registro.presion_arterial_dia >= 90:
            elevadas += 1

    if preclinica and preclinica not in preclinicas:
        if (preclinica.presion_arterial_sis and preclinica.presion_arterial_sis >= 140) or (
            preclinica.presion_arterial_dia and preclinica.presion_arterial_dia >= 90
        ):
            elevadas = max(elevadas, 1)

    if elevadas >= 3:
        return {
            "tipo": "hta",
            "nivel": "alto",
            "mensaje": "Posible hipertension - TA elevada en tres mediciones recientes",
        }
    if elevadas >= 1:
        return {
            "tipo": "hta",
            "nivel": "medio",
            "mensaje": "Riesgo de hipertension - confirmar con nuevas mediciones",
        }
    return None


def evaluar_riesgos_cronicos(paciente, institucion, preclinica=None, consulta=None, cita=None):
    config = get_predictiva_config(institucion)
    if not config["habilitar_riesgo_cronico"]:
        return []

    alertas = []
    for evaluador in (evaluar_riesgo_diabetes, evaluar_riesgo_hta):
        resultado = evaluador(paciente, institucion, preclinica=preclinica)
        if resultado:
            alertas.append(resultado)
    return alertas


def sincronizar_alertas_riesgo(paciente, institucion, preclinica=None, consulta=None, cita=None):
    evaluaciones = evaluar_riesgos_cronicos(
        paciente, institucion, preclinica=preclinica, consulta=consulta, cita=cita
    )
    tipos_evaluados = {item["tipo"] for item in evaluaciones}
    AlertaRiesgoCronico.objects.filter(
        paciente=paciente,
        institucion=institucion,
        activa=True,
        tipo__in=["diabetes", "hta"],
    ).exclude(tipo__in=tipos_evaluados).update(activa=False)

    creadas = []
    for item in evaluaciones:
        AlertaRiesgoCronico.objects.filter(
            paciente=paciente,
            institucion=institucion,
            tipo=item["tipo"],
            activa=True,
        ).update(activa=False)
        creadas.append(
            AlertaRiesgoCronico.objects.create(
                paciente=paciente,
                institucion=institucion,
                tipo=item["tipo"],
                nivel=item["nivel"],
                mensaje=item["mensaje"],
                preclinica=preclinica,
                consulta=consulta,
                cita=cita or (preclinica.cita if preclinica else None),
                activa=True,
            )
        )
    return creadas


def alertas_activas_paciente(paciente, institucion):
    return AlertaRiesgoCronico.objects.filter(
        paciente=paciente,
        institucion=institucion,
        activa=True,
    ).order_by("-creado_en")
