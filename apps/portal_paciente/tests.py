"""Pruebas del portal del paciente (Fase 3)."""
from datetime import time, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, PASSWORD
from apps.pacientes.models import Paciente
from apps.portal_paciente.models import PerfilPaciente


class PortalPacienteTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.paciente = Paciente.objects.get(pk=1)
        self.profesional = Profesional.objects.get(pk=2)
        self.user = User.objects.create_user(
            username="jose.ramirez@demo.test",
            email="jose.ramirez@demo.test",
            password=PASSWORD,
            first_name="Jose",
            last_name="Ramirez",
        )
        self.perfil = PerfilPaciente.objects.create(
            institucion=self.institucion,
            usuario=self.user,
            paciente=self.paciente,
        )
        self.client = Client(**HOST)
        self.client.login(username="jose.ramirez@demo.test", password=PASSWORD)
        session = self.client.session
        session["institucion_id"] = self.institucion.id
        session.save()

    def test_portal_dashboard_redirect_from_home(self):
        response = self.client.get("/", **HOST)
        self.assertRedirects(response, "/portal/")

    def test_portal_mis_citas(self):
        response = self.client.get("/portal/citas/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mis citas")

    def test_portal_cancelar_cita(self):
        fecha = timezone.localdate() + timedelta(days=3)
        cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.profesional,
            fecha=fecha,
            hora=time(10, 0),
            estado="confirmada",
        )
        response = self.client.get(f"/portal/citas/{cita.pk}/cancelar/", **HOST)
        self.assertEqual(response.status_code, 302)
        cita.refresh_from_db()
        self.assertEqual(cita.estado, "cancelada")

    def test_portal_llegada_cita_hoy(self):
        cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.profesional,
            fecha=timezone.localdate(),
            hora=time(11, 0),
            estado="confirmada",
        )
        response = self.client.get(f"/portal/citas/{cita.pk}/llegada/", **HOST)
        self.assertEqual(response.status_code, 302)
        cita.refresh_from_db()
        self.assertEqual(cita.estado, "en_espera")

    def test_portal_exportar_hce_json(self):
        response = self.client.get("/portal/historia/exportar/json/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertIn("consultas", response.content.decode())

    def test_portal_exportar_hce_pdf(self):
        response = self.client.get("/portal/historia/exportar/pdf/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_portal_registro_nuevo_paciente(self):
        client = Client(**HOST)
        session = client.session
        session["institucion_id"] = self.institucion.id
        session.save()
        response = client.post(
            "/portal/registro/",
            {
                "documento": "999999999999",
                "nombre": "Nuevo",
                "apellido": "Paciente",
                "email": "nuevo.paciente@demo.test",
                "telefono": "9999-9999",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            PerfilPaciente.objects.filter(
                paciente__documento="999999999999",
                institucion=self.institucion,
            ).exists()
        )

    def test_staff_no_accede_portal_sin_perfil(self):
        client = Client(**HOST)
        client.login(username="medico.demo", password=PASSWORD)
        session = client.session
        session["institucion_id"] = self.institucion.id
        session.save()
        response = client.get("/portal/", **HOST)
        self.assertEqual(response.status_code, 302)

    def test_portal_login_paciente(self):
        client = Client(**HOST)
        response = client.post(
            "/portal/entrar/",
            {"username": "jose.ramirez@demo.test", "password": PASSWORD},
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/portal/", response.url)

    def test_portal_restablecer_clave(self):
        client = Client(**HOST)
        response = client.post(
            "/portal/restablecer-clave/",
            {
                "email": "jose.ramirez@demo.test",
                "documento": self.paciente.documento,
                "password1": "NuevaClave123!",
                "password2": "NuevaClave123!",
            },
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        client = Client(**HOST)
        self.assertTrue(
            client.login(username="jose.ramirez@demo.test", password="NuevaClave123!")
        )
