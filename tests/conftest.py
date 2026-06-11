import pytest
from django.contrib.auth.models import User

from apps.core.models import Especialidad, Institucion, Profesional


@pytest.fixture
def institucion(db):
    return Institucion.objects.create(
        nombre="Clinica Demo",
        subdominio="demo",
        tipo="privada",
        activo=True,
    )


@pytest.fixture
def especialidad(db, institucion):
    return Especialidad.objects.create(
        institucion=institucion,
        nombre="Medicina General",
        codigo="MG",
        nivel="primero",
        activo=True,
    )


@pytest.fixture
def admin_user(db, institucion, especialidad):
    user = User.objects.create_user(username="admin.test", password="testpass123")
    Profesional.objects.create(
        institucion=institucion,
        usuario=user,
        especialidad=especialidad,
        nombre="Admin Test",
        tipo="admin",
        activo=True,
    )
    return user
