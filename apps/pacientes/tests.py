"""Pruebas funcionales de pacientes (FUN-P*)."""
from django.db import IntegrityError
from django.test import TestCase

from apps.core.models import Institucion
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente


class PacienteFunctionalTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("recepcion.demo")
        self.institucion = Institucion.objects.get(pk=1)

    def test_fun_p01_listar_pacientes(self):
        response = self.client.get("/pacientes/", **{"HTTP_HOST": "xmedical.cloud"})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.context["pacientes"]), 1)

    def test_fun_p02_crear_paciente(self):
        before = Paciente.objects.count()
        response = self.client.post(
            "/pacientes/nuevo/",
            {
                "documento": "TEST-99001",
                "nombre": "Juan",
                "apellido": "Prueba",
                "sexo": "M",
                "activo": True,
            },
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Paciente.objects.count(), before + 1)
        self.assertTrue(Paciente.objects.filter(documento="TEST-99001").exists())

    def test_fun_p03_documento_duplicado(self):
        existing = Paciente.objects.filter(institucion=self.institucion).first()
        with self.assertRaises(IntegrityError):
            Paciente.objects.create(
                institucion=self.institucion,
                documento=existing.documento,
                nombre="Duplicado",
                apellido="Test",
            )

    def test_fun_p04_detalle_paciente(self):
        paciente = Paciente.objects.filter(institucion=self.institucion).first()
        response = self.client.get(f"/pacientes/{paciente.pk}/", **{"HTTP_HOST": "xmedical.cloud"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["paciente"].pk, paciente.pk)

    def test_fun_p05_editar_paciente(self):
        paciente = Paciente.objects.create(
            institucion=self.institucion,
            documento="EDIT-001",
            nombre="Original",
            apellido="Nombre",
            activo=True,
        )
        response = self.client.post(
            f"/pacientes/{paciente.pk}/editar/",
            {
                "documento": "EDIT-001",
                "nombre": "Actualizado",
                "apellido": "Nombre",
                "sexo": "M",
                "activo": True,
            },
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        paciente.refresh_from_db()
        self.assertEqual(paciente.nombre, "Actualizado")

    def test_fun_p06_historia_redirect(self):
        paciente = Paciente.objects.filter(institucion=self.institucion).first()
        response = self.client.get(
            f"/pacientes/{paciente.pk}/historia/",
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/consulta/historia/{paciente.pk}/", response.url)

    def test_paciente_str(self):
        paciente = Paciente.objects.first()
        self.assertEqual(str(paciente), f"{paciente.nombre} {paciente.apellido}")
