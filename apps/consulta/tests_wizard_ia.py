"""Pruebas de autosave y sugerencias IA en wizard (Fase 2)."""
import json
from datetime import time
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.consulta.services import sugerir_diagnosticos
from apps.core.ai_services import AIConfigurationError
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica


class WizardAutosaveTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("medico.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(16, 0),
            estado="confirmada",
        )
        Preclinica.objects.create(institucion=self.institucion, cita=self.cita, presion_arterial_sis=120)

    def test_autosave_guarda_motivo(self):
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/autosave/",
            {"step": 2, "motivo_consulta": "Cefalea intensa"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        consulta = Consulta.objects.get(cita=self.cita)
        self.assertEqual(consulta.motivo_consulta, "Cefalea intensa")

    def test_autosave_rechaza_paso_invalido(self):
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/autosave/",
            {"step": 5},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 400)


class WizardIASuggestionTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("medico.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(17, 0),
            estado="confirmada",
        )
        self.consulta = Consulta.objects.create(
            institucion=self.institucion,
            cita=self.cita,
            motivo_consulta="Dolor toracico",
            anamnesis="Opresion al esfuerzo",
            examen_fisico="Ruidos cardiacos ritmicos",
        )

    @override_settings(OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_sugerir_diagnostico_sin_ia(self):
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/sugerir-diagnostico/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["available"])

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o")
    def test_sugerir_diagnostico_con_mock(self):
        payload = json.dumps(
            [{"codigo": "I10", "nombre": "Hipertension esencial primaria", "justificacion": "Por cuadro clinico"}]
        )
        with patch("apps.consulta.services.AIClient.complete", return_value=payload):
            response = self.client.post(
                f"/consulta/cita/{self.cita.pk}/sugerir-diagnostico/",
                **{"HTTP_HOST": "xmedical.cloud"},
            )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["sugerencias"][0]["codigo"], "I10")

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o")
    def test_servicio_sugerir_diagnosticos(self):
        payload = json.dumps([{"codigo": "R51", "nombre": "Cefalea", "justificacion": "Sintoma principal"}])
        with patch("apps.consulta.services.AIClient.complete", return_value=payload):
            sugerencias = sugerir_diagnosticos(self.consulta, self.institucion)
        self.assertEqual(sugerencias[0]["codigo"], "R51")

    @override_settings(OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_servicio_ia_no_configurada(self):
        with self.assertRaises(AIConfigurationError):
            sugerir_diagnosticos(self.consulta, self.institucion)

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o")
    def test_wizard_paso5_muestra_boton_ia(self):
        response = self.client.get(
            f"/consulta/cita/{self.cita.pk}/paso/5/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sugerir diagnosticos")

    @override_settings(OPENAI_API_KEY="", OPENROUTER_API_KEY="")
    def test_wizard_paso5_oculta_ia_sin_config(self):
        response = self.client.get(
            f"/consulta/cita/{self.cita.pk}/paso/5/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "btn-sugerir-diagnostico")
