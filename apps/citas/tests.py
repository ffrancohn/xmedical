"""Pruebas funcionales de citas (FUN-C*)."""
from datetime import time

from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente


class CitaFunctionalTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("recepcion.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.paciente = Paciente.objects.filter(institucion=self.institucion).first()
        self.profesional = Profesional.objects.get(pk=2)
        self.fecha = timezone.localdate()

    def _cita_payload(self, hora="14:00"):
        return {
            "paciente": self.paciente.pk,
            "especialidad": 1,
            "profesional": self.profesional.pk,
            "fecha": self.fecha.isoformat(),
            "hora": hora,
            "estado": "pendiente",
        }

    def test_fun_c01_listar_citas(self):
        response = self.client.get("/citas/", **{"HTTP_HOST": "xmedical.cloud"})
        self.assertEqual(response.status_code, 200)

    def test_fun_c02_agendar_cita(self):
        before = Cita.objects.count()
        response = self.client.post(
            "/citas/agendar/",
            self._cita_payload("14:00"),
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cita.objects.count(), before + 1)

    def test_fun_c03_slot_duplicado(self):
        self.client.post(
            "/citas/agendar/",
            self._cita_payload("15:00"),
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        response = self.client.post(
            "/citas/agendar/",
            self._cita_payload("15:00"),
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_fun_c04_cancelar_cita(self):
        cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.profesional,
            fecha=self.fecha,
            hora=time(16, 0),
            estado="pendiente",
        )
        response = self.client.get(
            f"/citas/{cita.pk}/cancelar/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        cita.refresh_from_db()
        self.assertEqual(cita.estado, "cancelada")

    def test_fun_c05_calendario_contexto(self):
        response = self.client.get(
            "/citas/?vista=semana",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("semana", response.context)
        self.assertEqual(len(response.context["semana"]), 7)
