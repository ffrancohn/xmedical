import json
from unittest.mock import patch

import pytest
from django.test import Client, override_settings
from django.urls import reverse

from apps.core.ai_institution_config import get_institution_ai_settings, save_institution_ai_settings
from apps.core.forms import ConfiguracionIAForm
from apps.core.models import Profesional
from apps.core.test_utils import HOST

PASSWORD = "testpass123"


def test_configuracion_ia_form_requires_ollama_url():
    form = ConfiguracionIAForm(
        data={
            "provider": "ollama",
            "ollama_base_url": "",
            "model": "llama3.2:3b",
            "temperature": "0.2",
        }
    )
    assert not form.is_valid()
    assert "ollama_base_url" in form.errors


def test_configuracion_ia_form_normalizes_url():
    form = ConfiguracionIAForm(
        data={
            "provider": "ollama",
            "ollama_base_url": "localhost:11434",
            "model": "llama3.2:3b",
            "temperature": "0.2",
        }
    )
    assert form.is_valid(), form.errors
    assert form.cleaned_data["ollama_base_url"] == "http://localhost:11434"


@pytest.fixture
def medico_user(db, institucion, especialidad):
    from django.contrib.auth.models import User

    user = User.objects.create_user(username="medico.test", password=PASSWORD)
    Profesional.objects.create(
        institucion=institucion,
        usuario=user,
        especialidad=especialidad,
        nombre="Medico Test",
        tipo="medico",
        activo=True,
    )
    return user


def _login(client, user):
    assert client.login(username=user.username, password=PASSWORD), "Login falló"


@pytest.mark.django_db
def test_configuracion_ia_form_save(institucion):
    form = ConfiguracionIAForm(
        data={
            "provider": "ollama",
            "ollama_base_url": "http://localhost:11434",
            "model": "llama3.2:3b",
            "vision_model": "llava:7b",
            "temperature": "0.3",
            "enabled": "on",
            "feature_diagnostico_sugerido": "on",
            "feature_resumen_clinico": "on",
            "feature_ocr_asistido": "on",
        }
    )
    assert form.is_valid(), form.errors
    save_institution_ai_settings(institucion, form.cleaned_data)
    institucion.refresh_from_db()
    cfg = get_institution_ai_settings(institucion)
    assert cfg["provider"] == "ollama"
    assert cfg["model"] == "llama3.2:3b"
    assert cfg["temperature"] == 0.3
    assert cfg["features"]["ocr_asistido"] is True


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="openai",
    OLLAMA_BASE_URL="http://localhost:11434",
    OLLAMA_MODEL="llama3.2:3b",
)
def test_configuracion_ia_admin_get(admin_user, institucion):
    client = Client(**HOST)
    _login(client, admin_user)
    client.session["institucion_id"] = institucion.id
    client.session.save()
    response = client.get(reverse("configuracion_ia"))
    assert response.status_code == 200
    assert "Configuración de Inteligencia Artificial" in response.content.decode()


@pytest.mark.django_db
def test_configuracion_ia_denied_for_medico(medico_user, institucion):
    client = Client(**HOST)
    _login(client, medico_user)
    client.session["institucion_id"] = institucion.id
    client.session.save()
    response = client.get(reverse("configuracion_ia"))
    assert response.status_code == 302
    assert response.url == reverse("dashboard")


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="openai",
    OLLAMA_BASE_URL="http://localhost:11434",
    OLLAMA_MODEL="llama3.2:3b",
)
def test_configuracion_ia_post_save(admin_user, institucion):
    client = Client(**HOST)
    _login(client, admin_user)
    client.session["institucion_id"] = institucion.id
    client.session.save()
    response = client.post(
        reverse("configuracion_ia"),
        {
            "provider": "ollama",
            "ollama_base_url": "http://ollama:11434",
            "model": "mistral:7b",
            "vision_model": "llava:7b",
            "temperature": "0.2",
            "enabled": "on",
            "feature_diagnostico_sugerido": "on",
        },
    )
    assert response.status_code == 302
    institucion.refresh_from_db()
    assert institucion.configuracion["ai"]["provider"] == "ollama"
    assert institucion.configuracion["ai"]["model"] == "mistral:7b"


@pytest.mark.django_db
def test_configuracion_ia_probar_mock(admin_user, institucion):
    client = Client(**HOST)
    _login(client, admin_user)
    mock_result = {"ok": True, "latency_ms": 120, "models": ["llama3.2:3b"], "model_configured": True}
    with patch("apps.core.views_ai._ollama_from_request_data") as factory:
        factory.return_value.health_check.return_value = mock_result
        response = client.post(
            reverse("configuracion_ia_probar"),
            data=json.dumps(
                {
                    "provider": "ollama",
                    "ollama_base_url": "http://localhost:11434",
                    "model": "llama3.2:3b",
                }
            ),
            content_type="application/json",
        )
    assert response.status_code == 200
    assert response.json()["ok"] is True


@pytest.mark.django_db
def test_configuracion_ia_modelos_mock(admin_user, institucion):
    client = Client(**HOST)
    _login(client, admin_user)
    with patch("apps.core.views_ai.OllamaProvider") as provider_cls:
        provider_cls.return_value.list_models.return_value = ["llama3.2:3b", "llava:7b"]
        response = client.get(
            reverse("configuracion_ia_modelos"),
            {"base_url": "http://localhost:11434", "model": "llama3.2:3b"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "llava:7b" in data["models"]
