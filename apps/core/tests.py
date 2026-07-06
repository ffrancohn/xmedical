"""
Pruebas funcionales de XMedical.
Ejecutar: python manage.py test apps.core
"""
from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.pacientes.models import Paciente

PASSWORD = "Xmedical123!"
HOST = {"HTTP_HOST": "xmedical.cloud"}


class FixtureLoadedTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_fixture_data_loaded(self):
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Institucion.objects.count(), 1)
        self.assertEqual(Profesional.objects.count(), 4)
        self.assertEqual(Paciente.objects.count(), 10)
        self.assertEqual(Cita.objects.count(), 3)


class AuthTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_login_page_accessible(self):
        response = Client(**HOST).get("/auth/login/", **HOST)
        self.assertEqual(response.status_code, 200)

    def test_protected_route_redirects_to_login(self):
        response = Client(**HOST).get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/auth/login/", response.url)

    def test_demo_users_can_login(self):
        for username in [
            "superadmin.demo",
            "admin.demo",
            "medico.demo",
            "enfermera.demo",
            "recepcion.demo",
        ]:
            client = Client(**HOST)
            self.assertTrue(
                client.login(username=username, password=PASSWORD),
                f"Login falló para {username}",
            )


class RoleRoutingTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_medico_sees_dashboard(self):
        client = Client(**HOST)
        client.login(username="medico.demo", password=PASSWORD)
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 200)

    def test_superadmin_redirects_to_superadmin_panel(self):
        client = Client(**HOST)
        client.login(username="superadmin.demo", password=PASSWORD)
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/superadmin/", response.url)

    def test_recepcionista_redirects_to_citas(self):
        client = Client(**HOST)
        client.login(username="recepcion.demo", password=PASSWORD)
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/citas/", response.url)

    def test_enfermera_redirects_to_preclinica(self):
        client = Client(**HOST)
        client.login(username="enfermera.demo", password=PASSWORD)
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/preclinica/", response.url)


class ClinicalRouteTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_recepcionista_accesses_pacientes_and_citas(self):
        client = Client(**HOST)
        client.login(username="recepcion.demo", password=PASSWORD)
        self.assertEqual(client.get("/pacientes/", **HOST).status_code, 200)
        self.assertEqual(client.get("/citas/", **HOST).status_code, 200)

    def test_enfermera_accesses_preclinica(self):
        client = Client(**HOST)
        client.login(username="enfermera.demo", password=PASSWORD)
        self.assertEqual(client.get("/preclinica/", **HOST).status_code, 200)

    def test_superadmin_accesses_superadmin_panel(self):
        client = Client(**HOST)
        client.login(username="superadmin.demo", password=PASSWORD)
        self.assertEqual(client.get("/superadmin/", **HOST).status_code, 200)


class TenantMiddlewareTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_institucion_exists_for_demo(self):
        institucion = Institucion.objects.get(subdominio="demo")
        self.assertEqual(institucion.nombre, "Clinica Demo")
        self.assertTrue(institucion.activo)
