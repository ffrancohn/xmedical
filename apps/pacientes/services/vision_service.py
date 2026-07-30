import base64
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from django.conf import settings

from apps.core.ai_institution_config import (
    get_institution_ai_settings,
    get_ollama_vision_client,
    ocr_ia_habilitado,
    ocr_ollama_configured,
)
from apps.core.ai_services import AIConfigurationError, AIRequestError, _post_chat_completion


class VisionServiceError(Exception):
    """Error base para OCR/vision."""


@dataclass
class OCRResult:
    nombre: str = ""
    apellido: str = ""
    documento: str = ""
    fecha_nacimiento: Optional[str] = None
    confianza: float = 0.0
    proveedor: str = "manual"
    texto_raw: str = ""
    manual_fallback: bool = True

    def to_dict(self):
        return asdict(self)


def _parse_fecha(texto: str) -> Optional[str]:
    patrones = [
        r"(\d{2})[/-](\d{2})[/-](\d{4})",
        r"(\d{4})[/-](\d{2})[/-](\d{2})",
    ]
    for patron in patrones:
        match = re.search(patron, texto)
        if not match:
            continue
        grupos = match.groups()
        if len(grupos[0]) == 4:
            return f"{grupos[0]}-{grupos[1]}-{grupos[2]}"
        return f"{grupos[2]}-{grupos[1]}-{grupos[0]}"
    return None


def _parse_documento(texto: str) -> str:
    match = re.search(r"\b(\d{4}-?\d{4}-?\d{5}|\d{13,15})\b", texto)
    return match.group(1).replace("-", "") if match else ""


def parse_document_text(texto: str) -> OCRResult:
    """Parser heuristico para texto OCR sin proveedor externo."""
    lineas = [linea.strip() for linea in texto.splitlines() if linea.strip()]
    nombre = ""
    apellido = ""
    if lineas:
        partes = lineas[0].split()
        if len(partes) >= 2:
            nombre = partes[0]
            apellido = " ".join(partes[1:])
        elif len(partes) == 1:
            nombre = partes[0]
    documento = _parse_documento(texto)
    fecha = _parse_fecha(texto)
    confianza = 0.35 if any([nombre, documento, fecha]) else 0.0
    return OCRResult(
        nombre=nombre,
        apellido=apellido,
        documento=documento,
        fecha_nacimiento=fecha,
        confianza=confianza,
        proveedor="heuristico",
        texto_raw=texto,
        manual_fallback=confianza == 0.0,
    )


def _parse_ai_json(content: str) -> OCRResult:
    texto = content.strip()
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?|```$", "", texto, flags=re.MULTILINE).strip()
    data = json.loads(texto)
    return OCRResult(
        nombre=(data.get("nombre") or "").strip(),
        apellido=(data.get("apellido") or "").strip(),
        documento=(data.get("documento") or "").strip(),
        fecha_nacimiento=(data.get("fecha_nacimiento") or None),
        confianza=float(data.get("confianza") or 0.75),
        proveedor=data.get("proveedor") or "ia",
        texto_raw=content,
        manual_fallback=False,
    )


_OCR_VISION_PROMPT = (
    "Extrae datos de un documento de identidad (cedula o pasaporte). "
    "Responde SOLO JSON valido con claves: "
    "nombre, apellido, documento, fecha_nacimiento (YYYY-MM-DD), confianza (0-1)."
)


class VisionService:
    """Extrae datos de documentos de identidad mediante proveedores configurados."""

    def __init__(self, institucion=None):
        self.institucion = institucion
        self._settings = get_institution_ai_settings(institucion)

    def is_provider_configured(self, provider: str) -> bool:
        if provider == "ollama":
            return ocr_ollama_configured(self.institucion)
        if provider == "google":
            return bool(getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", ""))
        if provider == "aws":
            return bool(getattr(settings, "AWS_ACCESS_KEY_ID", "") and getattr(settings, "AWS_SECRET_ACCESS_KEY", ""))
        if provider == "openrouter":
            return bool(getattr(settings, "OPENROUTER_API_KEY", "") and getattr(settings, "OPENROUTER_MODEL", ""))
        if provider == "openai":
            return bool(getattr(settings, "OPENAI_API_KEY", "") and getattr(settings, "OPENAI_MODEL", ""))
        return False

    def available_providers(self) -> list[str]:
        if not ocr_ia_habilitado(self.institucion):
            return []
        providers: list[str] = []
        if ocr_ollama_configured(self.institucion):
            providers.append("ollama")
        orden = getattr(
            settings,
            "VISION_PROVIDER_ORDER",
            ["ollama", "openai", "openrouter", "google", "aws"],
        )
        for proveedor in orden:
            if proveedor == "ollama":
                continue
            if self.is_provider_configured(proveedor) and proveedor not in providers:
                providers.append(proveedor)
        return providers

    def provider_labels(self) -> list[str]:
        labels = {
            "ollama": "Ollama (local)",
            "openai": "OpenAI (cloud)",
            "openrouter": "OpenRouter (cloud)",
            "google": "Google Vision",
            "aws": "AWS Textract",
        }
        return [labels.get(p, p) for p in self.available_providers()]

    def extract_from_image(self, image_bytes: bytes, content_type: str = "image/jpeg") -> OCRResult:
        if not ocr_ia_habilitado(self.institucion):
            return OCRResult(manual_fallback=True, proveedor="manual")

        for proveedor in self.available_providers():
            try:
                if proveedor == "ollama":
                    return self._extract_with_ollama_vision(image_bytes)
                if proveedor in ("openai", "openrouter"):
                    return self._extract_with_ai_vision(image_bytes, content_type, proveedor)
                if proveedor == "google":
                    return self._extract_with_google_vision(image_bytes)
                if proveedor == "aws":
                    return self._extract_with_aws_textract(image_bytes)
            except (VisionServiceError, AIConfigurationError, AIRequestError):
                if proveedor == "ollama" and not self._settings.get("fallback_cloud"):
                    break
                continue
        return OCRResult(manual_fallback=True, proveedor="manual")

    def _extract_with_ollama_vision(self, image_bytes: bytes) -> OCRResult:
        client = get_ollama_vision_client(self.institucion)
        cfg = self._settings
        encoded = base64.b64encode(image_bytes).decode("ascii")
        content = client.complete_with_image(
            _OCR_VISION_PROMPT,
            encoded,
            model=cfg.get("vision_model") or getattr(settings, "OLLAMA_VISION_MODEL", ""),
            temperature=float(cfg.get("temperature", 0.1)),
        )
        resultado = _parse_ai_json(content)
        resultado.proveedor = "ollama"
        resultado.manual_fallback = False
        return resultado

    def _extract_with_ai_vision(self, image_bytes: bytes, content_type: str, provider: str) -> OCRResult:
        if provider == "openrouter":
            api_key = getattr(settings, "OPENROUTER_API_KEY", "")
            model = getattr(settings, "OPENROUTER_MODEL", "")
            base_url = getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": getattr(settings, "OPENROUTER_HTTP_REFERER", "http://localhost:8000"),
                "X-Title": getattr(settings, "OPENROUTER_APP_NAME", "XMedical"),
            }
        else:
            api_key = getattr(settings, "OPENAI_API_KEY", "")
            model = getattr(settings, "OPENAI_MODEL", "")
            base_url = getattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

        if not api_key or not model:
            raise AIConfigurationError("Proveedor IA vision no configurado.")

        encoded = base64.b64encode(image_bytes).decode("ascii")
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": _OCR_VISION_PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:{content_type};base64,{encoded}"}},
                    ],
                }
            ],
            "temperature": 0.1,
        }
        response = _post_chat_completion(f"{base_url.rstrip('/')}/chat/completions", headers, payload, timeout=60)
        content = response["choices"][0]["message"]["content"]
        resultado = _parse_ai_json(content)
        resultado.proveedor = provider
        resultado.manual_fallback = False
        return resultado

    def _extract_with_google_vision(self, image_bytes: bytes) -> OCRResult:
        try:
            from google.cloud import vision
        except ImportError as exc:
            raise VisionServiceError("google-cloud-vision no instalado.") from exc

        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        if response.error.message:
            raise VisionServiceError(response.error.message)
        texto = ""
        if response.text_annotations:
            texto = response.text_annotations[0].description
        resultado = parse_document_text(texto)
        resultado.proveedor = "google"
        resultado.confianza = max(resultado.confianza, 0.6)
        resultado.manual_fallback = False
        return resultado

    def _extract_with_aws_textract(self, image_bytes: bytes) -> OCRResult:
        try:
            import boto3
        except ImportError as exc:
            raise VisionServiceError("boto3 no instalado.") from exc

        client = boto3.client(
            "textract",
            aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", ""),
            region_name=getattr(settings, "AWS_REGION", "us-east-1"),
        )
        response = client.detect_document_text(Document={"Bytes": image_bytes})
        lineas = []
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE" and block.get("Text"):
                lineas.append(block["Text"])
        texto = "\n".join(lineas)
        resultado = parse_document_text(texto)
        resultado.proveedor = "aws"
        resultado.confianza = max(resultado.confianza, 0.6)
        resultado.manual_fallback = False
        return resultado

    @staticmethod
    def validar_imagen(archivo) -> None:
        content_type = getattr(archivo, "content_type", "") or ""
        if not content_type.startswith("image/"):
            raise VisionServiceError("Solo se permiten imagenes (JPG, PNG, WEBP).")
        if archivo.size > 5 * 1024 * 1024:
            raise VisionServiceError("La imagen no puede superar 5 MB.")
