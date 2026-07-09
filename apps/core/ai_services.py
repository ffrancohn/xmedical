import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

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


def get_ai_config(institucion=None) -> AIConfig:
    provider = getattr(settings, "AI_PROVIDER", "openai")
    model = ""

    if provider == "openrouter":
        model = getattr(settings, "OPENROUTER_MODEL", "")
    else:
        model = getattr(settings, "OPENAI_MODEL", "")

    if institucion and isinstance(institucion.configuracion, dict):
        ai_cfg = institucion.configuracion.get("ai", {})
        if isinstance(ai_cfg, dict):
            provider = ai_cfg.get("provider") or provider
            model = ai_cfg.get("model") or model

    if not model:
        if provider == "openrouter":
            model = getattr(settings, "OPENROUTER_MODEL", "")
        else:
            model = getattr(settings, "OPENAI_MODEL", "")

    return AIConfig(provider=provider, model=model)


def _extract_message_content(payload: dict) -> str:
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIRequestError("Respuesta IA invalida o vacia.") from exc


def _post_chat_completion(url: str, headers: dict, body: dict, timeout: int = 30) -> dict:
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
    if config.provider == "openrouter":
        return OpenRouterProvider(default_model=config.model)
    return OpenAIProvider(default_model=config.model)


class AIClient:
    """Cliente unificado para llamadas IA con configuracion global o por institucion."""

    def __init__(self, institucion=None):
        self.institucion = institucion
        self.config = get_ai_config(institucion)
        self.provider = build_provider(self.config)

    def is_available(self) -> bool:
        return self.provider.is_configured()

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if not self.is_available():
            raise AIConfigurationError(
                f"IA no disponible para el proveedor '{self.config.provider}'. "
                "Revisa las variables de entorno o la configuracion de la institucion."
            )
        return self.provider.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model or self.config.model,
            temperature=temperature,
        )
