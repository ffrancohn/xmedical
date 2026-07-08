"""Pruebas funcionales y unitarias de preclínica (FUN-PR*)."""
from datetime import time
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica


class PreclinicaFunctionalTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("enfermera.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(10, 30),
            estado="pendiente",
        )

    def test_fun_pr01_lista_cola(self):
        response = self.client.get("/preclinica/", **{"HTTP_HOST": "xmedical.cloud"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.cita, list(response.context["citas"]))

    def test_fun_pr02_registrar_signos(self):
        response = self.client.post(
            f"/preclinica/{self.cita.pk}/",
            {
                "presion_arterial_sis": 120,
                "presion_arterial_dia": 80,
                "frecuencia_cardiaca": 72,
                "temperatura": "36.5",
                "saturacion_o2": 98,
                "peso": "70.00",
                "talla": "1.70",
                "motivo_consulta": "Control",
                "triaje": "baja",
            },
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Preclinica.objects.filter(cita=self.cita).exists())
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.estado, "en_espera")


class PreclinicaAlertasTests(TestCase):
    fixtures = ["initial_data.json"]

    def _preclinica(self, **kwargs):
        cita = Cita.objects.first()
        defaults = {
            "institucion": cita.institucion,
            "cita": cita,
        }
        defaults.update(kwargs)
        return Preclinica(**defaults)

    def test_fun_pr03_alerta_pa_alta(self):
        obj = self._preclinica(presion_arterial_sis=150)
        self.assertIn("Presion sistolica elevada", obj.alertas())

    def test_fun_pr04_alerta_fiebre(self):
        obj = self._preclinica(temperatura=Decimal("39.0"))
        self.assertIn("Fiebre", obj.alertas())

    def test_fun_pr05_alerta_spo2_baja(self):
        obj = self._preclinica(saturacion_o2=90)
        self.assertIn("Saturacion de oxigeno baja", obj.alertas())
