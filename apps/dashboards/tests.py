"""Pruebas de dashboards avanzados (Fase 2)."""
from datetime import time

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Especialidad, Institucion, Profesional
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica
from apps.referencias.models import Referencia
from apps.dashboards.services import (
    administracion_dashboard_data,
    enfermeria_dashboard_data,
    especialista_dashboard_data,
)


class DashboardServicesTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.instituciones = Institucion.objects.filter(pk=self.institucion.pk)
        self.paciente = Paciente.objects.filter(institucion=self.institucion).first()
        self.medico = Profesional.objects.get(pk=2)
        self.hoy = timezone.localdate()

    def _crear_cita(self, hora, estado="confirmada"):
        return Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=self.medico,
            fecha=self.hoy,
            hora=hora,
            estado=estado,
        )

    def test_enfermeria_pendientes_y_alertas(self):
        cita_pendiente = self._crear_cita(time(8, 0))
        cita_evaluada = self._crear_cita(time(9, 0))
        Preclinica.objects.create(
            institucion=self.institucion,
            cita=cita_evaluada,
            presion_arterial_sis=150,
            presion_arterial_dia=95,
            temperatura="38.5",
            saturacion_o2=90,
        )
        data = enfermeria_dashboard_data(self.instituciones)
        self.assertEqual(data["total_pendientes"], 1)
        self.assertEqual(data["total_evaluados"], 1)
        self.assertGreaterEqual(data["total_alertas"], 1)

    def test_administracion_metricas(self):
        self._crear_cita(time(10, 0))
        self._crear_cita(time(11, 0), estado="cancelada")
        consulta_cita = self._crear_cita(time(12, 0), estado="atendida")
        Consulta.objects.create(institucion=self.institucion, cita=consulta_cita)
        data = administracion_dashboard_data(self.instituciones)
        self.assertEqual(data["citas_canceladas_hoy"], 1)
        self.assertEqual(data["consultas_atendidas_hoy"], 1)
        self.assertGreater(data["ocupacion_agenda"], 0)

    def test_especialista_referencias_y_agenda(self):
        especialidad = Especialidad.objects.create(
            institucion=self.institucion,
            nombre="Cardiologia",
            codigo="CAR",
            nivel="segundo",
        )
        cardiologo = Profesional.objects.create(
            institucion=self.institucion,
            usuario=User.objects.create_user("cardio.dash", password="Xmedical123!"),
            especialidad=especialidad,
            nombre="Dr. Cardio",
            tipo="medico",
        )
        consulta = Consulta.objects.create(
            institucion=self.institucion,
            cita=self._crear_cita(time(14, 0)),
        )
        Referencia.objects.create(
            institucion=self.institucion,
            consulta_origen=consulta,
            especialidad_destino=especialidad,
            medico_referente=self.medico,
            motivo="Dolor toracico",
            estado="pendiente",
        )
        cita_cardio = Cita.objects.create(
            institucion=self.institucion,
            paciente=self.paciente,
            profesional=cardiologo,
            fecha=self.hoy,
            hora=time(15, 0),
            estado="confirmada",
        )
        data = especialista_dashboard_data(self.instituciones, profesional=cardiologo)
        self.assertEqual(data["total_pendientes"], 1)
        self.assertEqual(data["total_citas_hoy"], 1)
        self.assertEqual(data["agenda_propia"].first().pk, cita_cardio.pk)


class DashboardViewsTests(TestCase):
    fixtures = ["initial_data.json"]

    def test_enfermera_redirige_a_dashboard_enfermeria(self):
        client = auth_client("enfermera.demo")
        response = client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboards/enfermeria/", response.url)

    def test_admin_redirige_a_dashboard_administracion(self):
        client = auth_client("admin.demo")
        response = client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboards/administracion/", response.url)

    def test_medico_general_mantiene_dashboard_medico(self):
        client = auth_client("medico.demo")
        response = client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_enfermera_accede_dashboard_enfermeria(self):
        client = auth_client("enfermera.demo")
        response = client.get("/dashboards/enfermeria/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard de enfermeria")

    def test_recepcionista_no_accede_dashboard_admin(self):
        client = auth_client("recepcion.demo")
        response = client.get("/dashboards/administracion/")
        self.assertEqual(response.status_code, 302)

    def test_especialista_segundo_nivel_dashboard(self):
        institucion = Institucion.objects.get(pk=1)
        especialidad = Especialidad.objects.create(
            institucion=institucion,
            nombre="Endocrinologia",
            codigo="END",
            nivel="segundo",
        )
        user = User.objects.create_user("endo.demo", password="Xmedical123!")
        Profesional.objects.create(
            institucion=institucion,
            usuario=user,
            especialidad=especialidad,
            nombre="Dr. Endo",
            tipo="medico",
        )
        client = auth_client("endo.demo")
        response = client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboards/especialista/", response.url)
        response = client.get("/dashboards/especialista/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard del especialista")
        self.assertContains(response, "El hilo de hoy")


class HiloTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.instituciones = Institucion.objects.filter(pk=self.institucion.pk)
        self.pacientes = list(Paciente.objects.filter(institucion=self.institucion).order_by("id")[:4])
        self.medico = Profesional.objects.get(pk=2)
        self.hoy = timezone.localdate()

    def _cita(self, paciente, hora, estado="confirmada"):
        return Cita.objects.create(
            institucion=self.institucion,
            paciente=paciente,
            profesional=self.medico,
            fecha=self.hoy,
            hora=hora,
            estado=estado,
        )

    def test_estaciones_del_dia(self):
        from apps.dashboards.hilo import hilo_del_dia

        self._cita(self.pacientes[0], time(18, 0), "confirmada")
        self._cita(self.pacientes[1], time(18, 20), "en_espera")
        medida = self._cita(self.pacientes[2], time(18, 40), "en_espera")
        Preclinica.objects.create(institucion=self.institucion, cita=medida)
        atendida = self._cita(self.pacientes[3], time(19, 0), "atendida")
        consulta = Consulta.objects.create(institucion=self.institucion, cita=atendida)
        especialidad = Especialidad.objects.create(
            institucion=self.institucion, nombre="Dermatologia", codigo="DER", nivel="segundo"
        )
        Referencia.objects.create(
            institucion=self.institucion,
            consulta_origen=consulta,
            especialidad_destino=especialidad,
            medico_referente=self.medico,
            motivo="Lesion",
            estado="pendiente",
        )

        data = hilo_del_dia(self.instituciones, "recepcion")
        por_id = {station["id"]: station for station in data["stations"]}
        self.assertIn(self.pacientes[0].nombre, por_id["agendar"]["people"][0]["nombre"])
        self.assertEqual(por_id["recibir"]["count"], 1)
        self.assertEqual(por_id["medir"]["count"], 1)
        self.assertEqual(por_id["recibir"]["people"][0]["nombre"], por_id["medir"]["people"][0]["nombre"])
        self.assertIn(self.pacientes[2].nombre, por_id["atender"]["people"][0]["nombre"])
        self.assertEqual(por_id["derivar"]["count"], 1)
        self.assertTrue(por_id["agendar"]["open"])
        self.assertTrue(por_id["recibir"]["open"])
        self.assertFalse(por_id["medir"]["open"])

        enfermeria = hilo_del_dia(self.instituciones, "enfermeria")
        medir = next(station for station in enfermeria["stations"] if station["id"] == "medir")
        self.assertTrue(medir["open"])
        self.assertTrue(medir["mine"])

    def test_paciente_no_ve_la_ocupacion(self):
        from apps.dashboards.hilo import hilo_paciente

        propio = self.pacientes[0]
        ajeno = self.pacientes[1]
        self._cita(propio, time(17, 0), "en_espera")
        self._cita(ajeno, time(17, 20), "en_espera")
        data = hilo_paciente(propio, self.institucion)
        self.assertTrue(data["personal"])
        texto = str(data)
        self.assertNotIn(ajeno.nombre, texto)
        self.assertNotIn(ajeno.apellido, texto)
        actual = next(station for station in data["stations"] if station["open"])
        self.assertEqual(actual["id"], "recibir")
        self.assertEqual(actual["avatar"]["nombre"], f"{propio.nombre} {propio.apellido}")

    def test_inicio_muestra_el_hilo_y_admin_no(self):
        recepcion = auth_client("recepcion.demo")
        respuesta = recepcion.get("/dashboard/")
        self.assertIn("/dashboards/recepcion/", respuesta.url)
        pagina = recepcion.get("/dashboards/recepcion/")
        self.assertContains(pagina, "El hilo de hoy")
        self.assertContains(pagina, "Agendar")

        enfermera = auth_client("enfermera.demo")
        self.assertContains(enfermera.get("/dashboards/enfermeria/"), "El hilo de hoy")

        medico = auth_client("medico.demo")
        self.assertContains(medico.get("/dashboard/"), "El hilo de hoy")

        admin = auth_client("admin.demo")
        self.assertNotContains(admin.get("/dashboards/administracion/"), "El hilo de hoy")
        self.assertNotContains(admin.get("/dashboards/enfermeria/"), "El hilo de hoy")

