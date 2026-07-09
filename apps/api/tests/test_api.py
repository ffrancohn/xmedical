"""Pruebas API REST (API-01..API-06)."""
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.test_utils import PASSWORD
from apps.pacientes.models import Paciente


class APIAuthTests(APITestCase):
    fixtures = ["initial_data.json", "security_two_tenants.json"]

    def test_api_01_login_retorna_jwt_con_claims(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {"username": "medico.demo", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["institucion_id"], 1)
        self.assertEqual(response.data["rol"], "medico")

    def test_api_02_sin_token_retorna_401(self):
        response = self.client.get("/api/v1/pacientes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class APIPacientesTests(APITestCase):
    fixtures = ["initial_data.json", "security_two_tenants.json"]

    def setUp(self):
        login = self.client.post(
            "/api/v1/auth/login/",
            {"username": "recepcion.demo", "password": PASSWORD},
            format="json",
        )
        self.token = login.data["access"]

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_api_03_lista_pacientes_solo_tenant(self):
        self._auth()
        response = self.client.get("/api/v1/pacientes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.data["results"]]
        self.assertIn(1, ids)
        self.assertNotIn(100, ids)

    def test_api_04_recepcionista_crea_paciente(self):
        self._auth()
        response = self.client.post(
            "/api/v1/pacientes/",
            {
                "documento": "API-TEST-001",
                "nombre": "Paciente",
                "apellido": "API",
                "sexo": "M",
                "activo": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Paciente.objects.filter(documento="API-TEST-001", institucion_id=1).exists())

    def test_api_05_medico_no_crea_paciente(self):
        login = self.client.post(
            "/api/v1/auth/login/",
            {"username": "medico.demo", "password": PASSWORD},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        response = self.client.post(
            "/api/v1/pacientes/",
            {
                "documento": "API-TEST-002",
                "nombre": "Bloqueado",
                "apellido": "Medico",
                "sexo": "M",
                "activo": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class APIRateLimitTests(APITestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        from rest_framework.throttling import UserRateThrottle

        from apps.api.dashboard.views import DashboardView

        class OnePerMinuteThrottle(UserRateThrottle):
            rate = "1/min"

        DashboardView.throttle_classes = [OnePerMinuteThrottle]

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
    def test_api_06_rate_limit_retorna_429(self):
        login = self.client.post(
            "/api/v1/auth/login/",
            {"username": "medico.demo", "password": PASSWORD},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        response1 = self.client.get("/api/v1/dashboard/")
        response2 = self.client.get("/api/v1/dashboard/")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class APICitasTests(APITestCase):
    fixtures = ["initial_data.json"]

    def test_recepcionista_lista_citas(self):
        login = self.client.post(
            "/api/v1/auth/login/",
            {"username": "recepcion.demo", "password": PASSWORD},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        response = self.client.get("/api/v1/citas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)
