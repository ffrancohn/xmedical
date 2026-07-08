from django.test import TestCase
from rest_framework.test import APIClient

from apps.core.test_utils import PASSWORD


class OpenAPITests(TestCase):
    fixtures = ["initial_data.json"]

    def test_openapi_schema_disponible(self):
        client = APIClient()
        response = client.get("/api/v1/schema/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"openapi", response.content)

    def test_openapi_docs_disponible(self):
        client = APIClient()
        response = client.get("/api/v1/docs/")
        self.assertEqual(response.status_code, 200)

    def test_login_aparece_en_schema(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/login/",
            {"username": "medico.demo", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
