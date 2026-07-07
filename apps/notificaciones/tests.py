"""Pruebas de recordatorios y notificaciones (Fase 2)."""
from datetime import datetime, time, timedelta
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.notificaciones.models import LogNotificacion, RecordatorioMedicamento
from apps.notificaciones.services import (
    citas_para_recordatorio,
    enviar_recordatorio_cita,
    enviar_recordatorio_medicamento,
    medicamentos_para_recordatorio,
    ya_notificada_cita,
)
from apps.notificaciones.tasks import enviar_recordatorios_citas, enviar_recordatorios_medicamentos
from apps.pacientes.models import Paciente


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class NotificacionesCitaTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.medico = Profesional.objects.get(pk=2)
        self.paciente = Paciente.objects.filter(institucion=self.institucion).first()
        self.paciente.email = "paciente@test.local"
        self.paciente.save(update_fields=["email"])
        self.now = timezone.make_aware(datetime(2026, 7, 7, 10, 0))
        objetivo = self.now + timedelta(hours=24)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.medico,
            fecha=objetivo.date(),
            hora=objetivo.time().replace(second=0, microsecond=0),
            estado="confirmada",
        )

    def test_detecta_cita_24h(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            citas = citas_para_recordatorio(24 * 60)
        self.assertIn(self.cita, citas)

    def test_envia_recordatorio_y_registra_log(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            enviado = enviar_recordatorio_cita(self.cita, "cita_24h")
        self.assertTrue(enviado)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(LogNotificacion.objects.filter(cita=self.cita, tipo="cita_24h", estado="enviado").exists())

    def test_no_duplica_recordatorio(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            enviar_recordatorio_cita(self.cita, "cita_24h")
            segundo = enviar_recordatorio_cita(self.cita, "cita_24h")
        self.assertFalse(segundo)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(ya_notificada_cita(self.cita, "cita_24h"))

    def test_omite_sin_email(self):
        self.paciente.email = ""
        self.paciente.save(update_fields=["email"])
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            enviado = enviar_recordatorio_cita(self.cita, "cita_24h")
        self.assertFalse(enviado)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(LogNotificacion.objects.filter(cita=self.cita, tipo="cita_24h", estado="omitido").exists())

    def test_task_recordatorios_citas(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            resultado = enviar_recordatorios_citas()
        self.assertEqual(resultado["cita_24h"], 1)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class NotificacionesMedicamentoTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.paciente = Paciente.objects.filter(institucion=self.institucion).first()
        self.paciente.email = "paciente@test.local"
        self.paciente.save(update_fields=["email"])
        self.now = timezone.make_aware(datetime(2026, 7, 7, 8, 30))
        self.recordatorio = RecordatorioMedicamento.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            medicamento="Metformina",
            dosis="500 mg",
            frecuencia="diario",
            hora_recordatorio=time(8, 0),
        )

    def test_detecta_medicamento_programado(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            pendientes = medicamentos_para_recordatorio()
        self.assertIn(self.recordatorio, pendientes)

    def test_envia_recordatorio_medicamento(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            with patch("apps.notificaciones.services.timezone.now", return_value=self.now):
                enviado = enviar_recordatorio_medicamento(self.recordatorio)
        self.assertTrue(enviado)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(
            LogNotificacion.objects.filter(
                recordatorio_medicamento=self.recordatorio,
                tipo="medicamento",
                estado="enviado",
            ).exists()
        )

    def test_task_recordatorios_medicamentos(self):
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            with patch("apps.notificaciones.services.timezone.now", return_value=self.now):
                total = enviar_recordatorios_medicamentos()
        self.assertEqual(total, 1)

    def test_respeta_recordatorios_desactivados_institucion(self):
        self.institucion.configuracion = {"recordatorios_activos": False}
        self.institucion.save(update_fields=["configuracion"])
        with patch("apps.notificaciones.services.timezone.localtime", return_value=self.now):
            pendientes = medicamentos_para_recordatorio()
        self.assertEqual(pendientes, [])
