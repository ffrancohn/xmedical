"""Pruebas del wizard de consulta (FUN-Q*)."""
from datetime import time

from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta, Diagnostico
from apps.consulta.wizard import CIE10_MVP
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica


class ConsultaWizardTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("medico.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(11, 0),
            estado="confirmada",
        )
        Preclinica.objects.create(
            institucion=self.institucion,
            cita=self.cita,
            presion_arterial_sis=120,
            presion_arterial_dia=80,
            temperatura="36.5",
        )

    def test_fun_q01_paso1_revisar_preclinica(self):
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/1/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/paso/2/", response.url)

    def test_fun_q02_paso2_motivo(self):
        self.client.post(f"/consulta/cita/{self.cita.pk}/paso/1/", **{"HTTP_HOST": "xmedical.cloud"})
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/2/",
            {"motivo_consulta": "Dolor de cabeza"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        consulta = Consulta.objects.get(cita=self.cita)
        self.assertEqual(consulta.motivo_consulta, "Dolor de cabeza")

    def test_fun_q03_paso3_anamnesis(self):
        Consulta.objects.create(institucion=self.institucion, cita=self.cita, motivo_consulta="Test")
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/3/",
            {"anamnesis": "Paciente refiere cefalea"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        consulta = Consulta.objects.get(cita=self.cita)
        self.assertEqual(consulta.anamnesis, "Paciente refiere cefalea")

    def test_fun_q04_paso4_examen_fisico(self):
        Consulta.objects.create(institucion=self.institucion, cita=self.cita)
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/4/",
            {"examen_fisico": "Normotenso, afebril"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        consulta = Consulta.objects.get(cita=self.cita)
        self.assertEqual(consulta.examen_fisico, "Normotenso, afebril")

    def test_fun_q05_paso5_diagnostico(self):
        Consulta.objects.create(institucion=self.institucion, cita=self.cita)
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/5/",
            {
                "codigo_cie10": "I10",
                "nombre": "Hipertension esencial primaria",
                "es_principal": True,
            },
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        consulta = Consulta.objects.get(cita=self.cita)
        self.assertTrue(Diagnostico.objects.filter(consulta=consulta, codigo_cie10="I10").exists())

    def test_fun_q06_paso6_plan(self):
        Consulta.objects.create(institucion=self.institucion, cita=self.cita)
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/6/",
            {"plan_terapeutico": "Reposo e hidratacion", "conducta": "alta"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        consulta = Consulta.objects.get(cita=self.cita)
        self.assertEqual(consulta.plan_terapeutico, "Reposo e hidratacion")

    def test_fun_q07_paso7_finalizar(self):
        Consulta.objects.create(
            institucion=self.institucion,
            cita=self.cita,
            motivo_consulta="Test",
            plan_terapeutico="Plan",
        )
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/7/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/", response.url)
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.estado, "atendida")

    def test_fun_q08_busqueda_cie10(self):
        response = self.client.get("/consulta/cie10/?q=I10", **{"HTTP_HOST": "xmedical.cloud"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(any(item["codigo"] == "I10" for item in data["results"]))

    def test_fun_q09_historia_clinica(self):
        paciente = self.cita.paciente
        response = self.client.get(
            f"/consulta/historia/{paciente.pk}/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["paciente"].pk, paciente.pk)


class CIE10SearchTests(TestCase):
    def test_cie10_mvp_filtra_por_codigo(self):
        results = [item for item in CIE10_MVP if "i10" in item["codigo"].lower()]
        self.assertEqual(len(results), 1)
