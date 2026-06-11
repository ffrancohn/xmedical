from datetime import date, time, timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from apps.citas.forms import CitaForm
from apps.citas.models import Cita
from apps.core.audit import serialize_instance
from apps.core.models import Horario, Institucion, LogAuditoria, Profesional
from apps.pacientes.models import Paciente


@pytest.mark.django_db
def test_public_patient_registration(client, institucion):
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    response = client.post(
        reverse("pacientes_registro_publico"),
        {
            "documento": "99999999",
            "nombre": "Juan",
            "apellido": "Publico",
            "telefono": "99998888",
            "email": "juan@example.com",
        },
    )
    assert response.status_code == 302
    assert Paciente.objects.filter(documento="99999999", institucion=institucion).exists()


@pytest.mark.django_db
def test_login_requires_institution_membership(client, institucion, especialidad):
    user = User.objects.create_user(username="medico.a", password="testpass123")
    Profesional.objects.create(
        institucion=institucion,
        usuario=user,
        especialidad=especialidad,
        nombre="Medico A",
        tipo="medico",
        activo=True,
    )
    otra = Institucion.objects.create(nombre="Otra", subdominio="otra", tipo="publica", activo=True)
    response = client.post(
        reverse("login"),
        {"username": "medico.a", "password": "testpass123", "institucion": otra.id},
    )
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_login_success_sets_institution(client, institucion, admin_user):
    response = client.post(
        reverse("login"),
        {"username": "admin.test", "password": "testpass123", "institucion": institucion.id},
    )
    assert response.status_code == 302
    assert client.session["institucion_id"] == institucion.id


@pytest.mark.django_db
def test_patient_search_by_phone(client, admin_user, institucion):
    Paciente.objects.create(
        institucion=institucion,
        documento="123",
        nombre="Ana",
        apellido="Lopez",
        telefono="55551234",
    )
    client.force_login(admin_user)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    response = client.get(reverse("pacientes_lista"), {"q": "5555"})
    assert response.status_code == 200
    assert "Ana" in response.content.decode()


@pytest.mark.django_db
def test_cancelacion_requiere_2_horas(client, admin_user, institucion, especialidad):
    Profesional.objects.filter(usuario=admin_user).update(tipo="recepcionista")
    medico_user = User.objects.create_user(username="medico", password="testpass123")
    medico = Profesional.objects.create(
        institucion=institucion,
        usuario=medico_user,
        especialidad=especialidad,
        nombre="Medico",
        tipo="medico",
        activo=True,
    )
    paciente = Paciente.objects.create(
        institucion=institucion, documento="1", nombre="P", apellido="X"
    )
    cita = Cita.objects.create(
        institucion=institucion,
        paciente=paciente,
        profesional=medico,
        fecha=timezone.localdate(),
        hora=(timezone.localtime() + timedelta(hours=1)).time(),
        estado="pendiente",
    )
    client.force_login(admin_user)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    response = client.get(reverse("citas_cancelar", args=[cita.id]))
    assert response.status_code == 302
    cita.refresh_from_db()
    assert cita.estado == "pendiente"


@pytest.mark.django_db
def test_cita_form_valida_horario(institucion, especialidad):
    medico_user = User.objects.create_user(username="med", password="x")
    medico = Profesional.objects.create(
        institucion=institucion,
        usuario=medico_user,
        especialidad=especialidad,
        nombre="Medico",
        tipo="medico",
        activo=True,
    )
    paciente = Paciente.objects.create(
        institucion=institucion, documento="2", nombre="P", apellido="Y"
    )
    Horario.objects.create(
        institucion=institucion,
        profesional=medico,
        dia_semana=date.today().weekday(),
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
        activo=True,
    )
    form = CitaForm(
        data={
            "paciente": paciente.id,
            "especialidad": especialidad.id,
            "profesional": medico.id,
            "fecha": date.today().isoformat(),
            "hora": "18:00",
            "estado": "pendiente",
        },
        institucion=institucion,
    )
    assert not form.is_valid()
    assert "horario" in str(form.errors).lower()


@pytest.mark.django_db
def test_auditoria_registra_creacion_paciente(institucion):
    paciente = Paciente.objects.create(
      institucion=institucion,
      documento="777",
      nombre="Audit",
      apellido="Test",
  )
    assert LogAuditoria.objects.filter(
        tabla_afectada="pacientes.paciente",
        accion="CREATE",
        registro_id=paciente.id,
    ).exists()


@pytest.mark.django_db
def test_serialize_instance_handles_fk(institucion):
    paciente = Paciente.objects.create(
        institucion=institucion,
        documento="888",
        nombre="Ser",
        apellido="Test",
    )
    data = serialize_instance(paciente)
    assert data["institucion"] == institucion.id
