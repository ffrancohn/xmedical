import json
import re
from typing import List

from apps.core.ai_services import AIClient, AIConfigurationError, AIRequestError
from apps.consulta.wizard import CIE10_MVP


def _parse_sugerencias_json(content: str) -> List[dict]:
    texto = content.strip()
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?|```$", "", texto, flags=re.MULTILINE).strip()
    data = json.loads(texto)
    if isinstance(data, dict) and "sugerencias" in data:
        data = data["sugerencias"]
    if not isinstance(data, list):
        raise ValueError("Formato de sugerencias invalido.")
    sugerencias = []
    for item in data[:3]:
        if not isinstance(item, dict):
            continue
        codigo = (item.get("codigo") or item.get("codigo_cie10") or "").strip()
        nombre = (item.get("nombre") or "").strip()
        if codigo and nombre:
            sugerencias.append(
                {
                    "codigo": codigo,
                    "nombre": nombre,
                    "justificacion": (item.get("justificacion") or "").strip(),
                }
            )
    return sugerencias


def _enriquecer_con_cie10(sugerencias: List[dict]) -> List[dict]:
    codigos = {item["codigo"].upper(): item for item in CIE10_MVP}
    resultado = []
    for sugerencia in sugerencias:
        oficial = codigos.get(sugerencia["codigo"].upper())
        if oficial:
            sugerencia = {**sugerencia, "codigo": oficial["codigo"], "nombre": oficial["nombre"]}
        resultado.append(sugerencia)
    return resultado


def sugerir_diagnosticos(consulta, institucion=None) -> List[dict]:
    """Sugiere diagnosticos usando solo motivo, anamnesis y examen fisico."""
    client = AIClient(institucion)
    if not client.is_available():
        raise AIConfigurationError("IA no configurada para sugerencias de diagnostico.")

    if not any([consulta.motivo_consulta, consulta.anamnesis, consulta.examen_fisico]):
        return []

    system_prompt = (
        "Eres un asistente clinico. Responde SOLO con JSON valido: "
        '[{"codigo":"CIE10","nombre":"descripcion","justificacion":"breve"}]. '
        "Maximo 3 sugerencias. No incluyas datos identificables del paciente. "
        "Las sugerencias son de apoyo, no diagnostico definitivo."
    )
    user_prompt = (
        f"Motivo de consulta:\n{consulta.motivo_consulta or 'No registrado'}\n\n"
        f"Anamnesis:\n{consulta.anamnesis or 'No registrada'}\n\n"
        f"Examen fisico:\n{consulta.examen_fisico or 'No registrado'}\n\n"
        "Sugiere diagnosticos CIE-10 probables."
    )
    try:
        content = client.complete(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.2)
        sugerencias = _parse_sugerencias_json(content)
        return _enriquecer_con_cie10(sugerencias)
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        raise AIRequestError(f"No se pudieron interpretar las sugerencias IA: {exc}") from exc
