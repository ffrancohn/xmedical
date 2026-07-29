"""Configuración IA por institución (Institucion.configuracion['ai'])."""
from __future__ import annotations

from typing import Any

from django.conf import settings

DEFAULT_AI_FEATURES = {
    "diagnostico_sugerido": True,
    "resumen_clinico": True,
    "ocr_asistido": True,
}

AI_PROVIDER_CHOICES = (
    ("openai", "OpenAI"),
    ("openrouter", "OpenRouter"),
    ("ollama", "Ollama (local)"),
)


def _default_model_for_provider(provider: str) -> str:
    if provider == "openrouter":
        return getattr(settings, "OPENROUTER_MODEL", "")
    if provider == "ollama":
        return getattr(settings, "OLLAMA_MODEL", "")
    return getattr(settings, "OPENAI_MODEL", "")


def default_ai_settings() -> dict[str, Any]:
    provider = getattr(settings, "AI_PROVIDER", "openai")
    return {
        "provider": provider,
        "model": _default_model_for_provider(provider),
        "vision_model": getattr(settings, "OLLAMA_VISION_MODEL", "llava:7b"),
        "ollama_base_url": getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434"),
        "temperature": 0.2,
        "enabled": True,
        "fallback_cloud": False,
        "features": dict(DEFAULT_AI_FEATURES),
    }


def get_institution_ai_settings(institucion) -> dict[str, Any]:
    defaults = default_ai_settings()
    if not institucion:
        return defaults
    raw = institucion.configuracion if isinstance(institucion.configuracion, dict) else {}
    cfg = raw.get("ai", {})
    if not isinstance(cfg, dict):
        cfg = {}
    merged = {**defaults, **cfg}
    feature_cfg = cfg.get("features") if isinstance(cfg.get("features"), dict) else {}
    merged["features"] = {**DEFAULT_AI_FEATURES, **feature_cfg}
    return merged


def save_institution_ai_settings(institucion, data: dict[str, Any]) -> None:
    configuracion = dict(institucion.configuracion or {})
    configuracion["ai"] = {
        "provider": data["provider"],
        "model": data["model"],
        "vision_model": data.get("vision_model", ""),
        "ollama_base_url": data.get("ollama_base_url", ""),
        "temperature": float(data.get("temperature", 0.2)),
        "enabled": bool(data.get("enabled", True)),
        "fallback_cloud": bool(data.get("fallback_cloud", False)),
        "features": {
            "diagnostico_sugerido": bool(data.get("feature_diagnostico_sugerido", True)),
            "resumen_clinico": bool(data.get("feature_resumen_clinico", True)),
            "ocr_asistido": bool(data.get("feature_ocr_asistido", True)),
        },
    }
    institucion.configuracion = configuracion
    institucion.save(update_fields=["configuracion"])
