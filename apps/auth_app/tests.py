"""Pruebas funcionales de autenticación (FUN-A*)."""
from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.auth_app.models import UserPreference
from apps.core.models import Institucion, Profesional
from apps.core.test_utils import HOST, PASSWORD
from apps.pacientes.models import Paciente
from apps.portal_paciente.models import PerfilPaciente


class AuthFunctionalTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_fun_a01_login_valido(self):
        client = Client(**HOST)
        response = client.post(
            "/auth/login/",
            {"username": "medico.demo", "password": PASSWORD},
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/", response.url)

    def test_fun_a02_login_invalido(self):
        client = Client(**HOST)
        response = client.post(
            "/auth/login/",
            {"username": "medico.demo", "password": "wrong-password"},
            **HOST,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    def test_fun_a03_logout(self):
        client = Client(**HOST)
        client.login(username="medico.demo", password=PASSWORD)
        response = client.get("/auth/logout/", **HOST)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/auth/login/", response.url)
        self.assertFalse(client.session.get("_auth_user_id"))

    def test_fun_a04_registro_profesional(self):
        client = Client(**HOST)
        client.login(username="admin.demo", password=PASSWORD)
        institucion = Institucion.objects.get(pk=1)
        before = User.objects.count()
        response = client.post(
            "/auth/registro/",
            {
                "username": "nuevo.medico",
                "first_name": "Nuevo",
                "last_name": "Medico",
                "email": "nuevo@test.com",
                "password1": "TestPass123!",
                "password2": "TestPass123!",
                "institucion": institucion.id,
                "especialidad": 1,
                "nombre": "Dr. Nuevo",
                "tipo": "medico",
                "registro_medico": "MED-9999",
            },
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), before + 1)
        self.assertTrue(Profesional.objects.filter(usuario__username="nuevo.medico").exists())

    def test_fun_a05_preferencias_visuales(self):
        client = Client(**HOST)
        client.login(username="medico.demo", password=PASSWORD)
        response = client.post(
            "/auth/preferencias/",
            {"theme": "dark"},
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        pref = UserPreference.objects.get(user__username="medico.demo")
        self.assertEqual(pref.theme, "dark")

    def test_paciente_login_sin_institucion(self):
        institucion = Institucion.objects.get(pk=1)
        paciente = Paciente.objects.create(
            institucion=institucion,
            documento="888888888888",
            nombre="Portal",
            apellido="Paciente",
            email="portal.paciente@test.com",
        )
        user = User.objects.create_user(
            username="portal.paciente@test.com",
            email="portal.paciente@test.com",
            password=PASSWORD,
        )
        PerfilPaciente.objects.create(
            institucion=institucion,
            usuario=user,
            paciente=paciente,
        )
        client = Client(**HOST)
        response = client.post(
            "/auth/login/",
            {"username": "portal.paciente@test.com", "password": PASSWORD},
            **HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/portal/", response.url)
