from datetime import date, time, timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.citas.models import Cita
from apps.citas.services import FlexibleAgendamientoService, SinTurnosDisponiblesError
from apps.core.models import Especialidad, Horario, Institucion, Profesional
from apps.pacientes.models import Paciente


@pytest.fixture
def medico_con_horario(db, institucion, especialidad):
    user = User.objects.create_user(username="med.flex", password="testpass123")
    profesional = Profesional.objects.create(
        institucion=institucion,
        usuario=user,
        especialidad=especialidad,
        nombre="Medico Flexible",
        tipo="medico",
        activo=True,
    )
    hoy = date.today()
    Horario.objects.create(
        institucion=institucion,
        profesional=profesional,
        dia_semana=hoy.weekday(),
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
        activo=True,
    )
    return profesional


@pytest.mark.django_db
def test_buscar_disponibilidad_respeta_jornada_manana(institucion, especialidad, medico_con_horario):
    service = FlexibleAgendamientoService(institucion)
    hoy = date.today()
    turnos = service.buscar_disponibilidad(medico_con_horario, hoy, hoy, "manana", especialidad)
    assert turnos
    assert all(turno.hora < time(12, 0) for turno in turnos)


@pytest.mark.django_db
def test_buscar_disponibilidad_excluye_citas_ocupadas(institucion, especialidad, medico_con_horario):
    paciente = Paciente.objects.create(
        institucion=institucion, documento="FLEX1", nombre="Luis", apellido="Diaz"
    )
    hoy = date.today()
    Cita.objects.create(
        institucion=institucion,
        paciente=paciente,
        profesional=medico_con_horario,
        fecha=hoy,
        hora=time(8, 0),
        estado="confirmada",
    )
    service = FlexibleAgendamientoService(institucion)
    turnos = service.buscar_disponibilidad(medico_con_horario, hoy, hoy, "manana", especialidad)
    assert all(not (turno.fecha == hoy and turno.hora == time(8, 0)) for turno in turnos)


@pytest.mark.django_db
def test_asignar_primer_turno_crea_cita_flexible(institucion, especialidad, medico_con_horario):
    paciente = Paciente.objects.create(
        institucion=institucion, documento="FLEX2", nombre="Marta", apellido="Luna"
    )
    hoy = date.today()
    service = FlexibleAgendamientoService(institucion)
    cita = service.asignar_primer_turno(
        paciente=paciente,
        especialidad=especialidad,
        fecha_inicio=hoy,
        fecha_fin=hoy + timedelta(days=7),
        jornada="manana",
        profesional=medico_con_horario,
    )
    assert cita.tipo_agendamiento == "flexible"
    assert cita.profesional == medico_con_horario
    assert cita.estado == "confirmada"


@pytest.mark.django_db
def test_asignar_primer_turno_sin_disponibilidad(institucion, especialidad, medico_con_horario):
    paciente = Paciente.objects.create(
        institucion=institucion, documento="FLEX3", nombre="Ana", apellido="Sol"
    )
    hoy = date.today()
    for hora in [
        time(8, 0),
        time(8, 20),
        time(8, 40),
        time(9, 0),
        time(9, 20),
        time(9, 40),
        time(10, 0),
        time(10, 20),
        time(10, 40),
        time(11, 0),
        time(11, 20),
        time(11, 40),
    ]:
        Cita.objects.create(
            institucion=institucion,
            paciente=paciente,
            profesional=medico_con_horario,
            fecha=hoy,
            hora=hora,
            estado="confirmada",
        )
    service = FlexibleAgendamientoService(institucion)
    with pytest.raises(SinTurnosDisponiblesError):
        service.asignar_primer_turno(
            paciente=paciente,
            especialidad=especialidad,
            fecha_inicio=hoy,
            fecha_fin=hoy,
            jornada="manana",
            profesional=medico_con_horario,
        )


@pytest.mark.django_db
def test_vista_agendamiento_flexible(client, institucion, especialidad, medico_con_horario):
    recepcion = User.objects.create_user(username="recep.flex", password="testpass123")
    Profesional.objects.create(
        institucion=institucion,
        usuario=recepcion,
        nombre="Recepcion",
        tipo="recepcionista",
        activo=True,
    )
    paciente = Paciente.objects.create(
        institucion=institucion, documento="FLEX4", nombre="Pedro", apellido="Rios"
    )
    client.force_login(recepcion)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    hoy = date.today()
    response = client.post(
        reverse("citas_agendar_flexible"),
        {
            "paciente": paciente.id,
            "especialidad": especialidad.id,
            "profesional": medico_con_horario.id,
            "fecha_inicio": hoy.isoformat(),
            "fecha_fin": (hoy + timedelta(days=3)).isoformat(),
            "jornada": "manana",
        },
    )
    assert response.status_code == 200
    assert Cita.objects.filter(paciente=paciente, tipo_agendamiento="flexible").exists()
