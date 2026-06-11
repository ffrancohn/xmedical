from datetime import date, time

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Especialidad, Horario, Institucion, Profesional
from apps.pacientes.models import Paciente
from apps.referencias.models import Contrarreferencia, Referencia


@pytest.fixture
def especialidad_segundo(db, institucion):
    return Especialidad.objects.create(
        institucion=institucion,
        nombre="Cardiologia",
        codigo="CAR",
        nivel="segundo",
        duracion_consulta_minutos=30,
        activo=True,
    )


@pytest.fixture
def medico_general(db, institucion, especialidad):
    user = User.objects.create_user(username="mg.test", password="testpass123")
    profesional = Profesional.objects.create(
        institucion=institucion,
        usuario=user,
        especialidad=especialidad,
        nombre="Medico General",
        tipo="medico",
        activo=True,
    )
    return profesional


@pytest.fixture
def cardiologo(db, institucion, especialidad_segundo):
    user = User.objects.create_user(username="cardio.test", password="testpass123")
    profesional = Profesional.objects.create(
        institucion=institucion,
        usuario=user,
        especialidad=especialidad_segundo,
        nombre="Dr. Cardiologo",
        tipo="medico",
        activo=True,
    )
    Horario.objects.create(
        institucion=institucion,
        profesional=profesional,
        dia_semana=date.today().weekday(),
        hora_inicio=time(8, 0),
        hora_fin=time(17, 0),
        activo=True,
    )
    return profesional


@pytest.fixture
def consulta_origen(db, institucion, medico_general):
    paciente = Paciente.objects.create(
        institucion=institucion, documento="REF001", nombre="Pedro", apellido="Ramos"
    )
    cita = Cita.objects.create(
        institucion=institucion,
        paciente=paciente,
        profesional=medico_general,
        fecha=date.today(),
        hora=time(9, 0),
        estado="atendida",
    )
    return Consulta.objects.create(
        institucion=institucion,
        cita=cita,
        motivo_consulta="Dolor toracico",
        conducta="referencia",
    )


@pytest.mark.django_db
def test_crear_referencia_desde_consulta(client, institucion, medico_general, consulta_origen, especialidad_segundo):
    client.force_login(medico_general.usuario)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    response = client.post(
        reverse("referencias_nueva", args=[consulta_origen.id]),
        {
            "especialidad_destino": especialidad_segundo.id,
            "prioridad": "alta",
            "motivo": "Sospecha de angina",
        },
    )
    assert response.status_code == 302
    referencia = Referencia.objects.get(consulta_origen=consulta_origen)
    assert referencia.estado == "pendiente"
    assert referencia.especialidad_destino == especialidad_segundo


@pytest.mark.django_db
def test_especialista_acepta_y_agenda_cita(
    client, institucion, medico_general, cardiologo, consulta_origen, especialidad_segundo
):
    referencia = Referencia.objects.create(
        institucion=institucion,
        consulta_origen=consulta_origen,
        especialidad_destino=especialidad_segundo,
        medico_referente=medico_general,
        motivo="Evaluacion cardiaca",
        prioridad="media",
    )
    client.force_login(cardiologo.usuario)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()

    response = client.post(reverse("referencias_aceptar", args=[referencia.id]), {"comentarios_especialista": "Acepto"})
    assert response.status_code == 302
    referencia.refresh_from_db()
    assert referencia.estado == "aceptada"
    assert referencia.especialista == cardiologo

    response = client.post(
        reverse("referencias_agendar", args=[referencia.id]),
        {"fecha": date.today().isoformat(), "hora": "10:00"},
    )
    assert response.status_code == 302
    referencia.refresh_from_db()
    assert referencia.cita_derivada is not None


@pytest.mark.django_db
def test_contrarreferencia_completa_flujo(
    client, institucion, medico_general, cardiologo, consulta_origen, especialidad_segundo
):
    cita = Cita.objects.create(
        institucion=institucion,
        paciente=consulta_origen.cita.paciente,
        profesional=cardiologo,
        fecha=date.today(),
        hora=time(11, 0),
        estado="atendida",
    )
    referencia = Referencia.objects.create(
        institucion=institucion,
        consulta_origen=consulta_origen,
        especialidad_destino=especialidad_segundo,
        medico_referente=medico_general,
        especialista=cardiologo,
        cita_derivada=cita,
        estado="aceptada",
        motivo="Evaluacion",
    )
    client.force_login(cardiologo.usuario)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()

    response = client.post(
        reverse("referencias_contrarreferencia", args=[referencia.id]),
        {
            "resumen_atencion": "Sin hallazgos agudos",
            "plan_seguimiento": "Control en medicina general en 2 semanas",
        },
    )
    assert response.status_code == 302
    referencia.refresh_from_db()
    assert referencia.estado == "completada"
    assert Contrarreferencia.objects.filter(referencia=referencia).exists()


@pytest.mark.django_db
def test_rechazar_referencia(client, institucion, cardiologo, medico_general, consulta_origen, especialidad_segundo):
    referencia = Referencia.objects.create(
        institucion=institucion,
        consulta_origen=consulta_origen,
        especialidad_destino=especialidad_segundo,
        medico_referente=medico_general,
        motivo="Evaluacion",
    )
    client.force_login(cardiologo.usuario)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    response = client.post(
        reverse("referencias_rechazar", args=[referencia.id]),
        {"comentarios_especialista": "No corresponde a cardiologia"},
    )
    assert response.status_code == 302
    referencia.refresh_from_db()
    assert referencia.estado == "rechazada"
