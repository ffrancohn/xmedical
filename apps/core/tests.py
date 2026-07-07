"""
Pruebas funcionales de XMedical.
Ejecutar: python manage.py test apps.core
"""
from datetime import time

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.middleware import TenantMiddleware
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, PASSWORD, auth_client
from apps.pacientes.models import Paciente

PASSWORD = PASSWORD
HOST = HOST


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

    def test_enfermera_redirects_to_dashboard_enfermeria(self):
        client = Client(**HOST)
        client.login(username="enfermera.demo", password=PASSWORD)
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboards/enfermeria/", response.url)

    def test_admin_redirects_to_dashboard_administracion(self):
        client = Client(**HOST)
        client.login(username="admin.demo", password=PASSWORD)
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboards/administracion/", response.url)


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

    def test_fun_k01_tenant_middleware_subdominio(self):
        factory = RequestFactory()
        request = factory.get("/", HTTP_HOST="demo.xmedical.cloud")
        request.session = {}
        TenantMiddleware(lambda r: r)(request)
        self.assertEqual(request.institucion.subdominio, "demo")


class SmokeHttpTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_smk07_medico_dashboard(self):
        client = auth_client("medico.demo")
        self.assertEqual(client.get("/dashboard/", **HOST).status_code, 200)

    def test_smk08_recepcion_pacientes_citas(self):
        client = auth_client("recepcion.demo")
        self.assertEqual(client.get("/pacientes/", **HOST).status_code, 200)
        self.assertEqual(client.get("/citas/", **HOST).status_code, 200)

    def test_smk09_enfermera_preclinica(self):
        client = auth_client("enfermera.demo")
        self.assertEqual(client.get("/preclinica/", **HOST).status_code, 200)

    def test_smk10_superadmin_panel(self):
        client = auth_client("superadmin.demo")
        self.assertEqual(client.get("/superadmin/", **HOST).status_code, 200)

    def test_smk11_admin_registro(self):
        client = auth_client("admin.demo")
        self.assertEqual(client.get("/auth/registro/", **HOST).status_code, 200)


class CoreFunctionalTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_fun_k02_superadmin_filtro_instituciones(self):
        client = auth_client("superadmin.demo")
        response = client.get("/pacientes/?instituciones=1", **HOST)
        self.assertEqual(response.status_code, 200)
        for paciente in response.context["pacientes"]:
            self.assertEqual(paciente.institucion_id, 1)

    def test_fun_k03_dashboard_medico_citas_hoy(self):
        institucion = Institucion.objects.get(pk=1)
        medico = Profesional.objects.get(pk=2)
        Cita.objects.create(
            institucion=institucion,
            paciente=Paciente.objects.first(),
            profesional=medico,
            fecha=timezone.localdate(),
            hora=time(9, 30),
            estado="pendiente",
        )
        client = auth_client("medico.demo")
        response = client.get("/dashboard/", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.context["citas_hoy"]), 1)

    def test_fun_k04_home_autenticado_redirect(self):
        client = auth_client("medico.demo")
        response = client.get("/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/", response.url)
