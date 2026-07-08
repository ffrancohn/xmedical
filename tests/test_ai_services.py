from unittest.mock import patch

import pytest
from django.test import override_settings

from apps.core.ai_services import (
    AIClient,
    AIConfigurationError,
    OpenAIProvider,
    OpenRouterProvider,
    get_ai_config,
)


@pytest.mark.django_db
def test_get_ai_config_uses_institution_over_global(institucion):
    institucion.configuracion = {"ai": {"provider": "openrouter", "model": "anthropic/claude-3-haiku"}}
    institucion.save(update_fields=["configuracion"])

    with override_settings(AI_PROVIDER="openai", OPENAI_MODEL="gpt-4o-mini", OPENROUTER_MODEL=""):
        config = get_ai_config(institucion)

    assert config.provider == "openrouter"
    assert config.model == "anthropic/claude-3-haiku"


@override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENAI_MODEL="")
def test_ai_client_not_available_without_keys():
    client = AIClient()
    assert client.is_available() is False
    with pytest.raises(AIConfigurationError):
        client.complete("system", "user")


@override_settings(
    AI_PROVIDER="openai",
    OPENAI_API_KEY="test-key",
    OPENAI_MODEL="gpt-4o-mini",
)
def test_openai_provider_complete_with_mock():
    provider = OpenAIProvider()
    mock_response = {"choices": [{"message": {"content": "Diagnostico sugerido"}}]}

    with patch("apps.core.ai_services._post_chat_completion", return_value=mock_response) as mocked:
        result = provider.complete("Eres medico", "Paciente con fiebre")

    assert result == "Diagnostico sugerido"
    mocked.assert_called_once()
    args = mocked.call_args[0]
    assert args[0].endswith("/chat/completions")
    assert args[2]["model"] == "gpt-4o-mini"


@override_settings(
    AI_PROVIDER="openrouter",
    OPENROUTER_API_KEY="router-key",
    OPENROUTER_MODEL="meta-llama/llama-3-8b",
)
def test_openrouter_provider_complete_with_mock():
    provider = OpenRouterProvider()
    mock_response = {"choices": [{"message": {"content": "Resumen clinico"}}]}

    with patch("apps.core.ai_services._post_chat_completion", return_value=mock_response):
        result = provider.complete("Resume", "Motivo: dolor abdominal")

    assert result == "Resumen clinico"


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="openai",
    OPENAI_API_KEY="test-key",
    OPENAI_MODEL="gpt-4o-mini",
)
def test_ai_client_uses_institution_model(institucion):
    institucion.configuracion = {"ai": {"model": "gpt-4.1-mini"}}
    institucion.save(update_fields=["configuracion"])
    client = AIClient(institucion=institucion)
    mock_response = {"choices": [{"message": {"content": "ok"}}]}

    with patch("apps.core.ai_services._post_chat_completion", return_value=mock_response) as mocked:
        client.complete("system", "user")

    assert mocked.call_args[0][2]["model"] == "gpt-4.1-mini"


@override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENAI_MODEL="gpt-4o-mini")
def test_openai_provider_requires_api_key():
    provider = OpenAIProvider()
    assert provider.is_configured() is False
    with pytest.raises(AIConfigurationError):
        provider.complete("system", "user")
