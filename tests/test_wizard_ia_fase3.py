"""Pruebas Fase 3: wizard consulta con config IA por institución (Ollama)."""
import json
from datetime import time
from unittest.mock import patch

import pytest
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.consulta.services import ia_diagnostico_disponible, sugerir_diagnosticos
from apps.core.ai_institution_config import save_institution_ai_settings
from apps.core.ai_services import AIClient, AIConfigurationError, AIRequestError, build_cloud_fallback_provider
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, auth_client
from apps.pacientes.models import Paciente


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="openai",
    OPENAI_API_KEY="",
    OLLAMA_BASE_URL="http://localhost:11434",
    OLLAMA_MODEL="llama3.2:3b",
)
def test_ia_diagnostico_disponible_con_ollama_institucion(institucion):
    save_institution_ai_settings(
        institucion,
        {
            "provider": "ollama",
            "ollama_base_url": "http://localhost:11434",
            "model": "llama3.2:3b",
            "vision_model": "",
            "temperature": 0.2,
            "enabled": True,
            "fallback_cloud": False,
            "feature_diagnostico_sugerido": True,
            "feature_resumen_clinico": True,
            "feature_ocr_asistido": True,
        },
    )
    assert ia_diagnostico_disponible(institucion) is True


@pytest.mark.django_db
@override_settings(OPENAI_API_KEY="key", OPENAI_MODEL="gpt-4o-mini")
def test_ia_diagnostico_no_disponible_si_feature_desactivada(institucion):
    save_institution_ai_settings(
        institucion,
        {
            "provider": "openai",
            "ollama_base_url": "",
            "model": "gpt-4o-mini",
            "vision_model": "",
            "temperature": 0.2,
            "enabled": True,
            "fallback_cloud": False,
            "feature_diagnostico_sugerido": False,
            "feature_resumen_clinico": True,
            "feature_ocr_asistido": True,
        },
    )
    assert ia_diagnostico_disponible(institucion) is False


@override_settings(OPENAI_API_KEY="fb-key", OPENAI_MODEL="gpt-4o-mini", OPENROUTER_API_KEY="")
def test_complete_with_fallback_ollama_a_openai():
    client = AIClient()
    client.config = client.config.__class__(
        provider="ollama",
        model="llama3.2:3b",
        ollama_base_url="http://localhost:11434",
        fallback_cloud=True,
    )
    client.provider = client.provider.__class__(default_model="llama3.2:3b")

    payload = '[{"codigo":"I10","nombre":"Hipertension","justificacion":"x"}]'
    with patch.object(client, "complete", side_effect=AIRequestError("Ollama caido")):
        with patch("apps.core.ai_services.build_cloud_fallback_provider") as fallback_factory:
            fallback = build_cloud_fallback_provider()
            fallback_factory.return_value = fallback
            with patch.object(fallback, "complete", return_value=payload) as cloud_complete:
                content, provider = client.complete_with_fallback("sys", "user")

    assert provider == "openai"
    assert content == payload
    cloud_complete.assert_called_once()


class WizardOllamaIntegrationTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("medico.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(18, 0),
            estado="confirmada",
        )
        self.consulta = Consulta.objects.create(
            institucion=self.institucion,
            cita=self.cita,
            motivo_consulta="Dolor toracico",
            anamnesis="Opresion al esfuerzo",
            examen_fisico="Ruidos cardiacos ritmicos",
        )
        self.institucion.configuracion = {
            "ai": {
                "provider": "ollama",
                "model": "llama3.2:3b",
                "ollama_base_url": "http://localhost:11434",
                "temperature": 0.2,
                "enabled": True,
                "fallback_cloud": False,
                "features": {"diagnostico_sugerido": True, "resumen_clinico": True, "ocr_asistido": True},
            }
        }
        self.institucion.save(update_fields=["configuracion"])

    @override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_wizard_paso6_muestra_ia_ollama_sin_api_cloud(self):
        response = self.client.get(
            f"/consulta/cita/{self.cita.pk}/paso/6/",
            **HOST,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "btn-sugerir-diagnostico")
        self.assertContains(response, "Local (llama3.2:3b)")

    @override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_sugerir_diagnostico_ollama_mock(self):
        payload = json.dumps(
            [{"codigo": "I20", "nombre": "Angina de pecho", "justificacion": "Dolor toracico"}]
        )
        with patch(
            "apps.consulta.services.AIClient.complete_with_fallback",
            return_value=(payload, "ollama"),
        ):
            response = self.client.post(
                f"/consulta/cita/{self.cita.pk}/sugerir-diagnostico/",
                **HOST,
            )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["provider"], "ollama")
        self.assertEqual(data["sugerencias"][0]["codigo"], "I20")

    @override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_servicio_sugerir_con_ollama_institucion(self):
        payload = json.dumps([{"codigo": "R51", "nombre": "Cefalea", "justificacion": "Sintoma"}])
        with patch(
            "apps.consulta.services.AIClient.complete_with_fallback",
            return_value=(payload, "ollama"),
        ):
            sugerencias, meta = sugerir_diagnosticos(self.consulta, self.institucion)
        self.assertEqual(sugerencias[0]["codigo"], "R51")
        self.assertEqual(meta["provider"], "ollama")

    @override_settings(AI_PROVIDER="openai", OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_feature_desactivada_oculta_boton(self):
        cfg = dict(self.institucion.configuracion)
        cfg["ai"] = {**cfg["ai"], "features": {"diagnostico_sugerido": False}}
        self.institucion.configuracion = cfg
        self.institucion.save(update_fields=["configuracion"])
        response = self.client.get(
            f"/consulta/cita/{self.cita.pk}/paso/6/",
            **HOST,
        )
        self.assertNotContains(response, "btn-sugerir-diagnostico")
