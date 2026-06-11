from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Profesional
from apps.pacientes.models import Paciente
from apps.qr.models import DocumentoQR
from apps.qr.services import QRExpiradoError, QRNoEncontradoError, QRService, QRYaUsadoError


@pytest.fixture
def consulta_con_cita(db, institucion, especialidad, admin_user):
    medico = Profesional.objects.get(usuario=admin_user)
    paciente = Paciente.objects.create(
        institucion=institucion, documento="QR001", nombre="Luis", apellido="QR"
    )
    cita = Cita.objects.create(
        institucion=institucion,
        paciente=paciente,
        profesional=medico,
        fecha=timezone.localdate(),
        hora=timezone.localtime().time(),
        estado="atendida",
    )
    return Consulta.objects.create(
        institucion=institucion,
        cita=cita,
        plan_terapeutico="Reposo y analgesicos",
        conducta="alta",
    )


@pytest.mark.django_db
def test_generar_receta_crea_documento(consulta_con_cita):
    service = QRService(institucion=consulta_con_cita.institucion)
    doc = service.generar_receta(consulta_con_cita)
    assert doc.tipo == "receta"
    assert doc.token
    assert doc.paciente == consulta_con_cita.cita.paciente
    assert doc.expira_en > timezone.now()


@pytest.mark.django_db
def test_validar_rechaza_vencido(consulta_con_cita):
    service = QRService()
    doc = service.generar_examen(consulta_con_cita)
    doc.expira_en = timezone.now() - timedelta(days=1)
    doc.save(update_fields=["expira_en"])
    resultado = service.validar(doc.token)
    assert resultado["estado"] == "vencido"


@pytest.mark.django_db
def test_marcar_usado_checkin_actualiza_cita(consulta_con_cita):
    consulta_con_cita.cita.estado = "confirmada"
    consulta_con_cita.cita.save(update_fields=["estado"])
    service = QRService()
    doc = service.generar_checkin(consulta_con_cita.cita)
    service.marcar_usado(doc)
    doc.refresh_from_db()
    consulta_con_cita.cita.refresh_from_db()
    assert doc.usado is True
    assert consulta_con_cita.cita.estado == "en_espera"


@pytest.mark.django_db
def test_marcar_usado_rechaza_duplicado(consulta_con_cita):
    service = QRService()
    doc = service.generar_receta(consulta_con_cita)
    service.marcar_usado(doc)
    with pytest.raises(QRYaUsadoError):
        service.marcar_usado(doc)


@pytest.mark.django_db
def test_validar_token_inexistente():
    service = QRService()
    with pytest.raises(QRNoEncontradoError):
        service.validar("token-que-no-existe")


@pytest.mark.django_db
@patch("apps.qr.services.QRService.generar_imagen_base64", return_value="aW1n")
def test_generar_qr_desde_consulta(mock_img, client, consulta_con_cita, admin_user, institucion):
    client.force_login(admin_user)
    session = client.session
    session["institucion_id"] = institucion.id
    session.save()
    response = client.post(reverse("qr_generar", args=[consulta_con_cita.id, "receta"]))
    assert response.status_code == 302
    assert DocumentoQR.objects.filter(consulta=consulta_con_cita, tipo="receta").exists()


@pytest.mark.django_db
def test_vista_validacion_publica(consulta_con_cita):
    service = QRService()
    doc = service.generar_receta(consulta_con_cita)
    client = __import__("django.test", fromlist=["Client"]).Client()
    response = client.get(reverse("qr_validar", args=[doc.token]))
    assert response.status_code == 200
    assert "valido" in response.content.decode("utf-8").lower()


@pytest.mark.django_db
def test_marcar_usado_rechaza_vencido(consulta_con_cita):
    service = QRService()
    doc = service.generar_receta(consulta_con_cita)
    doc.expira_en = timezone.now() - timedelta(hours=1)
    doc.save(update_fields=["expira_en"])
    with pytest.raises(QRExpiradoError):
        service.marcar_usado(doc)
