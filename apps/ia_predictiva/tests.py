"""Pruebas de modelos predictivos (Fase 3)."""
from datetime import time, timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, auth_client
from apps.ia_predictiva.models import AlertaRiesgoCronico, DemandaCita, PrediccionAusentismo
from apps.ia_predictiva.services import (
    calcular_demanda_institucion,
    calcular_probabilidad_ausentismo,
    evaluar_riesgo_diabetes,
    reentrenar_ausentismo_institucion,
    sincronizar_alertas_riesgo,
)
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica


class AusentismoPredictivoTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.paciente = Paciente.objects.get(pk=1)
        self.profesional = Profesional.objects.get(pk=2)

    def _crear_cita(self, **kwargs):
        defaults = {
            "institucion": self.institucion,
            "paciente": self.paciente,
            "profesional": self.profesional,
            "fecha": timezone.localdate() + timedelta(days=3),
            "hora": time(10, 0),
            "estado": "pendiente",
        }
        defaults.update(kwargs)
        return Cita.objects.create(**defaults)

    def test_prediccion_automatica_al_crear_cita(self):
        cita = self._crear_cita()
        self.assertTrue(hasattr(cita, "prediccion_ausentismo"))
        self.assertIsNotNone(cita.prediccion_ausentismo)

    def test_probabilidad_aumenta_con_historial_cancelaciones(self):
        for _ in range(3):
            Cita.objects.create(
                institucion=self.institucion,
                paciente=self.paciente,
                profesional=self.profesional,
                fecha=timezone.localdate() - timedelta(days=10),
                hora=time(9, 0),
                estado="cancelada",
            )
        cita = self._crear_cita()
        prob, nivel, _ = calcular_probabilidad_ausentismo(cita)
        self.assertGreaterEqual(prob, Decimal("40"))
        self.assertIn(nivel, ("medio", "alto"))

    def test_reentrenamiento_actualiza_predicciones(self):
        cita = self._crear_cita()
        PrediccionAusentismo.objects.filter(cita=cita).delete()
        actualizadas = reentrenar_ausentismo_institucion(self.institucion)
        self.assertGreater(actualizadas, 0)
        self.assertTrue(PrediccionAusentismo.objects.filter(cita=cita).exists())


class DemandaPredictivaTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)

    def test_calcular_demanda_institucion(self):
        actualizadas = calcular_demanda_institucion(self.institucion)
        self.assertGreater(actualizadas, 0)
        self.assertTrue(DemandaCita.objects.filter(institucion=self.institucion).exists())


class RiesgoCronicoTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.paciente = Paciente.objects.get(pk=1)
        self.profesional = Profesional.objects.get(pk=2)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.profesional,
            fecha=timezone.localdate(),
            hora=time(8, 0),
            estado="confirmada",
        )

    def test_riesgo_diabetes_imc_alto(self):
        preclinica = Preclinica.objects.create(
            institucion=self.institucion,
            cita=self.cita,
            imc=Decimal("32.5"),
        )
        resultado = evaluar_riesgo_diabetes(self.paciente, self.institucion, preclinica=preclinica)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["nivel"], "alto")

    def test_alerta_hta_tres_mediciones(self):
        for dias, hora in [(10, time(8, 0)), (5, time(9, 0)), (1, time(10, 0))]:
            cita = Cita.objects.create(
                institucion=self.institucion,
                paciente=self.paciente,
                profesional=self.profesional,
                fecha=timezone.localdate() - timedelta(days=dias),
                hora=hora,
                estado="atendida",
            )
            Preclinica.objects.create(
                institucion=self.institucion,
                cita=cita,
                presion_arterial_sis=150,
                presion_arterial_dia=95,
            )
        alertas = sincronizar_alertas_riesgo(self.paciente, self.institucion)
        self.assertTrue(any(a.tipo == "hta" and a.nivel == "alto" for a in alertas))
        self.assertTrue(AlertaRiesgoCronico.objects.filter(paciente=self.paciente, tipo="hta").exists())


class DashboardPredictivoIntegrationTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_dashboard_admin_muestra_seccion_predictiva(self):
        client = auth_client("admin.demo")
        response = client.get("/dashboards/administracion/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alertas de ausentismo predictivo")
        self.assertContains(response, "Demanda esperada")
