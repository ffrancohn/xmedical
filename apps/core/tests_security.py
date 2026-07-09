"""Pruebas de seguridad (SEC-*)."""
import unittest
from datetime import time

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, PASSWORD, auth_client
from apps.pacientes.models import Paciente


SECURITY_FIXTURES = ["initial_data.json", "security_two_tenants.json"]


class SQLInjectionTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_01_sqli_busqueda_pacientes(self):
        client = auth_client("recepcion.demo")
        before = Paciente.objects.filter(institucion_id=1).count()
        response = client.get("/pacientes/?q=' OR '1'='1", **HOST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Paciente.objects.count(), Paciente.objects.count())
        self.assertLessEqual(len(response.context["pacientes"]), before)


class XSSTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_02_xss_almacenado_paciente(self):
        client = auth_client("recepcion.demo")
        payload = "<script>alert(1)</script>"
        response = client.post(
            "/pacientes/nuevo/",
            {
                "documento": "XSS-SEC-001",
                "nombre": payload,
                "apellido": "Test",
                "sexo": "M",
                "activo": True,
            },
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        paciente = Paciente.objects.get(documento="XSS-SEC-001")
        detail = client.get(f"/pacientes/{paciente.pk}/", **HOST)
        self.assertNotIn(payload, detail.content.decode())
        self.assertIn("&lt;script&gt;", detail.content.decode())


class CSRFTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_03_csrf_crear_paciente(self):
        client = auth_client("recepcion.demo")
        client = Client(enforce_csrf_checks=True, **HOST)
        client.login(username="recepcion.demo", password=PASSWORD)
        response = client.post(
            "/pacientes/nuevo/",
            {
                "documento": "CSRF-001",
                "nombre": "Sin",
                "apellido": "Token",
                "sexo": "M",
                "activo": True,
            },
            **HOST,
        )
        self.assertEqual(response.status_code, 403)


class AuthBypassTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_04_rutas_protegidas_sin_sesion(self):
        client = Client(**HOST)
        for path in ["/dashboard/", "/pacientes/", "/superadmin/"]:
            response = client.get(path, **HOST)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/auth/login/", response.url)


class TenantIsolationTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_05_usuario_no_ve_paciente_otro_tenant(self):
        client = auth_client("medico.demo")
        response = client.get("/pacientes/100/", **HOST)
        self.assertEqual(response.status_code, 404)

    def test_sec_05_lista_no_incluye_otro_tenant(self):
        client = auth_client("recepcion.demo")
        response = client.get("/pacientes/", **HOST)
        ids = [p.pk for p in response.context["pacientes"]]
        self.assertNotIn(100, ids)


class RateLimitTests(TestCase):
    def test_sec_06_rate_limiting_configurado(self):
        rf = settings.REST_FRAMEWORK
        self.assertIn("DEFAULT_THROTTLE_CLASSES", rf)
        self.assertIn("user", rf["DEFAULT_THROTTLE_RATES"])
        self.assertEqual(rf["DEFAULT_THROTTLE_RATES"]["user"], "100/min")


class RBACStrictTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_13_enfermera_no_accede_consulta(self):
        client = auth_client("enfermera.demo")
        response = client.get("/consulta/cita/1/paso/1/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard/")

    def test_sec_14_recepcionista_no_accede_preclinica(self):
        client = auth_client("recepcion.demo")
        response = client.get("/preclinica/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard/")

    def test_sec_15_medico_no_crea_pacientes(self):
        client = auth_client("medico.demo")
        response = client.get("/pacientes/nuevo/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard/")

    def test_sec_15_enfermera_no_ve_historia_clinica(self):
        client = auth_client("enfermera.demo")
        response = client.get("/consulta/historia/1/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard/")


class RBACTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_07_medico_no_puede_backup(self):
        client = auth_client("medico.demo")
        response = client.post("/superadmin/backup/", {"alcance": "global"}, **HOST)
        self.assertIn(response.status_code, [302, 403])


class IDORTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_09_no_cancelar_cita_otro_tenant(self):
        client = auth_client("medico.demo")
        response = client.get("/citas/100/cancelar/", **HOST)
        self.assertIn(response.status_code, [302, 404])
        cita = Cita.objects.get(pk=100)
        self.assertEqual(cita.estado, "pendiente")


class UnauthenticatedEndpointTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_10_cie10_requiere_login(self):
        client = Client(**HOST)
        response = client.get("/consulta/cie10/?q=I10", **HOST)
        self.assertIn(response.status_code, [302, 403])

    def test_sec_10_historia_requiere_login(self):
        client = Client(**HOST)
        response = client.get("/consulta/historia/1/", **HOST)
        self.assertIn(response.status_code, [302, 403])


@override_settings(DEBUG=False, SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True)
class CookieSecurityTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_11_session_cookie_flags(self):
        client = Client(**HOST)
        response = client.post(
            "/auth/login/",
            {"username": "medico.demo", "password": PASSWORD},
            **HOST,
        )
        cookie = response.cookies.get("sessionid")
        self.assertIsNotNone(cookie)
        self.assertTrue(cookie.get("secure"))
        self.assertTrue(cookie.get("httponly"))


class ClickjackingTests(TestCase):
    fixtures = SECURITY_FIXTURES

    def test_sec_12_x_frame_options(self):
        client = Client(**HOST)
        response = client.get("/auth/login/", **HOST)
        self.assertIn(response.headers.get("X-Frame-Options", "").upper(), ["DENY", "SAMEORIGIN"])
