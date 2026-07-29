from unittest.mock import patch

import pytest
from django.test import override_settings

from apps.core.ai_services import (
    AIClient,
    AIConfigurationError,
    AIRequestError,
    OllamaProvider,
    OpenAIProvider,
    OpenRouterProvider,
    build_provider,
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


@pytest.mark.django_db
def test_get_ai_config_ollama_from_institution(institucion):
    institucion.configuracion = {"ai": {"provider": "ollama", "model": "mistral:7b"}}
    institucion.save(update_fields=["configuracion"])

    with override_settings(AI_PROVIDER="openai", OLLAMA_MODEL="llama3.2:3b"):
        config = get_ai_config(institucion)

    assert config.provider == "ollama"
    assert config.model == "mistral:7b"


@override_settings(AI_PROVIDER="ollama", OLLAMA_MODEL="llama3.2:3b", OLLAMA_BASE_URL="http://localhost:11434")
def test_get_ai_config_ollama_global():
    config = get_ai_config()
    assert config.provider == "ollama"
    assert config.model == "llama3.2:3b"


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


@override_settings(
    AI_PROVIDER="ollama",
    OLLAMA_BASE_URL="http://localhost:11434",
    OLLAMA_MODEL="llama3.2:3b",
)
def test_ollama_provider_complete_with_mock():
    provider = OllamaProvider()
    mock_response = {"message": {"role": "assistant", "content": "Diagnostico sugerido local"}}

    with patch("apps.core.ai_services._post_json", return_value=mock_response) as mocked:
        result = provider.complete("Eres medico", "Paciente con fiebre")

    assert result == "Diagnostico sugerido local"
    mocked.assert_called_once()
    url, headers, body = mocked.call_args[0]
    assert url == "http://localhost:11434/api/chat"
    assert body["model"] == "llama3.2:3b"
    assert body["stream"] is False


@override_settings(OLLAMA_BASE_URL="http://localhost:11434", OLLAMA_MODEL="llama3.2:3b")
def test_ollama_list_models():
    provider = OllamaProvider()
    mock_tags = {"models": [{"name": "llama3.2:3b"}, {"name": "llava:7b"}]}

    with patch("apps.core.ai_services._get_json", return_value=mock_tags):
        models = provider.list_models()

    assert models == ["llama3.2:3b", "llava:7b"]


@override_settings(OLLAMA_BASE_URL="http://localhost:11434", OLLAMA_MODEL="llama3.2:3b")
def test_ollama_health_check_ok():
    provider = OllamaProvider()
    mock_tags = {"models": [{"name": "llama3.2:3b"}]}

    with patch("apps.core.ai_services._get_json", return_value=mock_tags):
        with patch.object(provider, "complete", return_value="OK"):
            result = provider.health_check()

    assert result["ok"] is True
    assert result["model_configured"] is True
    assert "llama3.2:3b" in result["models"]


@override_settings(OLLAMA_BASE_URL="http://localhost:11434", OLLAMA_MODEL="llama3.2:3b")
def test_ollama_health_check_connection_error():
    provider = OllamaProvider()

    with patch("apps.core.ai_services._get_json", side_effect=AIRequestError("No se pudo conectar")):
        result = provider.health_check(probe_chat=False)

    assert result["ok"] is False
    assert "No se pudo conectar" in result["error"]


@override_settings(OLLAMA_BASE_URL="", OLLAMA_MODEL="")
def test_ollama_provider_requires_model():
    provider = OllamaProvider()
    assert provider.is_configured() is False
    with pytest.raises(AIConfigurationError):
        provider.complete("system", "user")


@override_settings(AI_PROVIDER="ollama", OLLAMA_BASE_URL="http://localhost:11434", OLLAMA_MODEL="llama3.2:3b")
def test_build_provider_ollama():
    from apps.core.ai_services import AIConfig

    provider = build_provider(AIConfig(provider="ollama", model="llama3.2:3b"))
    assert isinstance(provider, OllamaProvider)


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


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="ollama",
    OLLAMA_BASE_URL="http://localhost:11434",
    OLLAMA_MODEL="llama3.2:3b",
)
def test_ai_client_ollama_available(institucion):
    client = AIClient(institucion=institucion)
    assert client.is_available() is True
    assert isinstance(client.provider, OllamaProvider)


@override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENAI_MODEL="gpt-4o-mini")
def test_openai_provider_requires_api_key():
    provider = OpenAIProvider()
    assert provider.is_configured() is False
    with pytest.raises(AIConfigurationError):
        provider.complete("system", "user")
