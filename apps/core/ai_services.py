import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional

from django.conf import settings


class AIProviderError(Exception):
    """Error base para integraciones IA."""


class AIConfigurationError(AIProviderError):
    """Falta configuracion o credenciales para el proveedor IA."""


class AIRequestError(AIProviderError):
    """Error al llamar al proveedor IA."""


@dataclass
class AIConfig:
    provider: str
    model: str
    ollama_base_url: str = ""
    vision_model: str = ""
    temperature: float = 0.2
    enabled: bool = True
    fallback_cloud: bool = False


def get_ai_config(institucion=None) -> AIConfig:
    from apps.core.ai_institution_config import get_institution_ai_settings

    cfg = get_institution_ai_settings(institucion)
    provider = cfg["provider"]
    model = cfg["model"] or ""

    if not model:
        if provider == "openrouter":
            model = getattr(settings, "OPENROUTER_MODEL", "")
        elif provider == "ollama":
            model = getattr(settings, "OLLAMA_MODEL", "")
        else:
            model = getattr(settings, "OPENAI_MODEL", "")

    return AIConfig(
        provider=provider,
        model=model,
        ollama_base_url=(cfg.get("ollama_base_url") or "").strip(),
        vision_model=(cfg.get("vision_model") or "").strip(),
        temperature=float(cfg.get("temperature", 0.2)),
        enabled=bool(cfg.get("enabled", True)),
        fallback_cloud=bool(cfg.get("fallback_cloud", False)),
    )


def _extract_message_content(payload: dict) -> str:
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIRequestError("Respuesta IA invalida o vacia.") from exc


def _extract_ollama_content(payload: dict) -> str:
    try:
        content = payload["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise AIRequestError("Respuesta Ollama invalida o vacia.") from exc
    if not str(content).strip():
        raise AIRequestError("Respuesta Ollama invalida o vacia.")
    return str(content)


def _get_json(url: str, timeout: int = 30) -> dict:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AIRequestError(f"Error HTTP {exc.code} del proveedor IA: {detail}") from exc
    except urllib.error.URLError as exc:
        raise AIRequestError(f"No se pudo conectar con el proveedor IA: {exc}") from exc


def _post_json(url: str, headers: dict, body: dict, timeout: int = 30) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AIRequestError(f"Error HTTP {exc.code} del proveedor IA: {detail}") from exc
    except urllib.error.URLError as exc:
        raise AIRequestError(f"No se pudo conectar con el proveedor IA: {exc}") from exc


def _post_chat_completion(url: str, headers: dict, body: dict, timeout: int = 30) -> dict:
    return _post_json(url, headers, body, timeout=timeout)


class BaseAIProvider:
    provider_name = "base"

    def __init__(self, api_key: str = "", default_model: str = "", base_url: str = ""):
        self.api_key = (api_key or "").strip()
        self.default_model = (default_model or "").strip()
        self.base_url = (base_url or "").rstrip("/")

    def is_configured(self) -> bool:
        return bool(self.api_key and self.default_model and self.base_url)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        raise NotImplementedError


class OpenAIProvider(BaseAIProvider):
    provider_name = "openai"

    def __init__(self, api_key: str = "", default_model: str = "", base_url: str = ""):
        super().__init__(
            api_key=api_key or getattr(settings, "OPENAI_API_KEY", ""),
            default_model=default_model or getattr(settings, "OPENAI_MODEL", ""),
            base_url=base_url or getattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )

    def is_configured(self) -> bool:
        return bool(self.api_key and self.default_model)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if not self.is_configured():
            raise AIConfigurationError("OpenAI no esta configurado. Define OPENAI_API_KEY y OPENAI_MODEL.")

        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = _post_chat_completion(f"{self.base_url}/chat/completions", headers, payload)
        return _extract_message_content(response)


class OllamaProvider(BaseAIProvider):
    provider_name = "ollama"

    def __init__(self, api_key: str = "", default_model: str = "", base_url: str = ""):
        super().__init__(
            api_key="",
            default_model=default_model or getattr(settings, "OLLAMA_MODEL", ""),
            base_url=base_url or getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434"),
        )
        self.timeout = getattr(settings, "OLLAMA_TIMEOUT", 120)

    def is_configured(self) -> bool:
        return bool(self.default_model and self.base_url)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if not self.is_configured():
            raise AIConfigurationError(
                "Ollama no esta configurado. Define OLLAMA_BASE_URL y OLLAMA_MODEL."
            )

        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature},
        }
        headers = {"Content-Type": "application/json"}
        response = _post_json(
            f"{self.base_url}/api/chat",
            headers,
            payload,
            timeout=self.timeout,
        )
        return _extract_ollama_content(response)

    def list_models(self) -> list[str]:
        if not self.base_url:
            raise AIConfigurationError("Ollama no esta configurado. Define OLLAMA_BASE_URL.")
        payload = _get_json(f"{self.base_url}/api/tags", timeout=min(self.timeout, 30))
        models = payload.get("models") or []
        return [item["name"] for item in models if isinstance(item, dict) and item.get("name")]

    def health_check(self, probe_chat: bool = True) -> dict[str, Any]:
        if not self.base_url:
            return {"ok": False, "error": "OLLAMA_BASE_URL no configurada"}

        started = time.monotonic()
        try:
            models = self.list_models()
        except AIRequestError as exc:
            return {"ok": False, "error": str(exc)}

        result: dict[str, Any] = {
            "ok": True,
            "latency_ms": int((time.monotonic() - started) * 1000),
            "models": models,
            "model_configured": self.default_model in models if self.default_model else False,
            "base_url": self.base_url,
        }

        if probe_chat and self.is_configured() and self.default_model in models:
            chat_started = time.monotonic()
            try:
                self.complete("Responde solo: OK", "ping", temperature=0)
                result["chat_latency_ms"] = int((time.monotonic() - chat_started) * 1000)
            except AIRequestError as exc:
                result["ok"] = False
                result["error"] = str(exc)

        return result


class OpenRouterProvider(BaseAIProvider):
    provider_name = "openrouter"

    def __init__(self, api_key: str = "", default_model: str = "", base_url: str = ""):
        super().__init__(
            api_key=api_key or getattr(settings, "OPENROUTER_API_KEY", ""),
            default_model=default_model or getattr(settings, "OPENROUTER_MODEL", ""),
            base_url=base_url or getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        )

    def is_configured(self) -> bool:
        return bool(self.api_key and self.default_model)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if not self.is_configured():
            raise AIConfigurationError(
                "OpenRouter no esta configurado. Define OPENROUTER_API_KEY y OPENROUTER_MODEL."
            )

        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": getattr(settings, "OPENROUTER_HTTP_REFERER", "http://localhost:8000"),
            "X-Title": getattr(settings, "OPENROUTER_APP_NAME", "XMedical"),
        }
        response = _post_chat_completion(f"{self.base_url}/chat/completions", headers, payload)
        return _extract_message_content(response)


def build_provider(config: AIConfig) -> BaseAIProvider:
    if config.provider == "ollama":
        kwargs = {"default_model": config.model}
        if config.ollama_base_url:
            kwargs["base_url"] = config.ollama_base_url
        return OllamaProvider(**kwargs)
    if config.provider == "openrouter":
        return OpenRouterProvider(default_model=config.model)
    return OpenAIProvider(default_model=config.model)


def build_cloud_fallback_provider() -> Optional[BaseAIProvider]:
    """Proveedor cloud de respaldo cuando Ollama falla (OpenRouter > OpenAI)."""
    openrouter = OpenRouterProvider()
    if openrouter.is_configured():
        return openrouter
    openai = OpenAIProvider()
    if openai.is_configured():
        return openai
    return None


class AIClient:
    """Cliente unificado para llamadas IA con configuracion global o por institucion."""

    def __init__(self, institucion=None):
        self.institucion = institucion
        self.config = get_ai_config(institucion)
        self.provider = build_provider(self.config)

    def is_available(self) -> bool:
        if not self.config.enabled:
            return False
        return self.provider.is_configured()

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        if not self.is_available():
            raise AIConfigurationError(
                f"IA no disponible para el proveedor '{self.config.provider}'. "
                "Revisa las variables de entorno o la configuracion de la institucion."
            )
        effective_temp = self.config.temperature if temperature is None else temperature
        return self.provider.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model or self.config.model,
            temperature=effective_temp,
        )

    def complete_with_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> tuple[str, str]:
        """Ejecuta complete(); si Ollama falla y fallback_cloud, usa proveedor cloud.

        Returns:
            (contenido, provider_usado)
        """
        try:
            return self.complete(system_prompt, user_prompt, model=model, temperature=temperature), self.config.provider
        except AIRequestError:
            if self.config.provider != "ollama" or not self.config.fallback_cloud:
                raise
            fallback = build_cloud_fallback_provider()
            if not fallback:
                raise
            effective_temp = self.config.temperature if temperature is None else temperature
            content = fallback.complete(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                temperature=effective_temp,
            )
            return content, fallback.provider_name
