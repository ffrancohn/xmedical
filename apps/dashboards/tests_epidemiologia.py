"""Pruebas del dashboard epidemiologico (Fase 3)."""
from datetime import time, timedelta

from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta, Diagnostico
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, auth_client
from apps.dashboards.epidemiologia import (
    detectar_alertas_brote,
    epidemiologia_dashboard_data,
    tendencias_diagnosticos,
)
from apps.pacientes.models import Paciente


class EpidemiologiaServicesTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.instituciones = Institucion.objects.filter(pk=self.institucion.pk)
        self.paciente = Paciente.objects.filter(institucion=self.institucion).first()
        self.medico = Profesional.objects.get(pk=2)

    def _consulta_con_diagnostico(self, dias_atras, codigo="J06.9", nombre="Infeccion respiratoria"):
        cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.medico,
            fecha=timezone.localdate() - timedelta(days=dias_atras),
            hora=time(9, 0),
            estado="atendida",
        )
        consulta = Consulta.objects.create(institucion=self.institucion, cita=cita)
        Consulta.objects.filter(pk=consulta.pk).update(
            creado_en=timezone.now() - timedelta(days=dias_atras)
        )
        return Diagnostico.objects.create(
            institucion=self.institucion,
            consulta=consulta,
            codigo_cie10=codigo,
            nombre=nombre,
            es_principal=True,
        )

    def test_detecta_brote_con_cinco_casos(self):
        for dias in range(5):
            self._consulta_con_diagnostico(dias)
        alertas = detectar_alertas_brote(self.instituciones)
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["codigo_cie10"], "J06.9")
        self.assertGreaterEqual(alertas[0]["total"], 5)

    def test_no_brote_con_pocos_casos(self):
        for dias in range(3):
            self._consulta_con_diagnostico(dias)
        alertas = detectar_alertas_brote(self.instituciones)
        self.assertEqual(len(alertas), 0)

    def test_tendencias_mensuales(self):
        self._consulta_con_diagnostico(5, codigo="I10", nombre="Hipertension")
        self._consulta_con_diagnostico(35, codigo="I10", nombre="Hipertension")
        data = tendencias_diagnosticos(self.instituciones, meses=3)
        self.assertTrue(data["series"])
        self.assertTrue(data["meses"])

    def test_dashboard_data_integracion(self):
        for dias in range(6):
            self._consulta_con_diagnostico(dias)
        data = epidemiologia_dashboard_data(self.instituciones)
        self.assertEqual(data["total_brotes"], 1)
        self.assertGreater(data["total_diagnosticos_mes"], 0)


class EpidemiologiaViewsTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_admin_accede_dashboard_epidemiologia(self):
        client = auth_client("admin.demo")
        response = client.get("/dashboards/epidemiologia/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard epidemiologico")

    def test_recepcionista_no_accede(self):
        client = auth_client("recepcion.demo")
        response = client.get("/dashboards/epidemiologia/", **HOST)
        self.assertEqual(response.status_code, 302)

    def test_superadmin_accede(self):
        client = auth_client("superadmin.demo")
        response = client.get("/dashboards/epidemiologia/", **HOST)
        self.assertEqual(response.status_code, 200)
