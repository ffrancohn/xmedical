from datetime import time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.citas.models import Cita
from apps.core.models import Especialidad, Espacio, Institucion, Profesional
from apps.core.plano import estado_plano
from apps.pacientes.models import Paciente


class PlanoEstadoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inst = Institucion.objects.create(nombre="Clinica Plano", subdominio="plano")
        cls.esp = Especialidad.objects.create(nombre="Medicina General", nivel="primero", institucion=cls.inst)
        cls.medico = Profesional.objects.create(
            usuario=User.objects.create_user("med", password="x"),
            nombre="Dr. Plano", tipo="medico", especialidad=cls.esp, institucion=cls.inst, activo=True,
        )
        cls.paciente = Paciente.objects.create(
            nombre="Ana", apellido="Prueba", documento="0001", institucion=cls.inst, activo=True,
        )
        cls.consulta = Espacio.objects.create(
            institucion=cls.inst, nombre="Consultorio 1", tipo="consultorio", x=1, y=1, ancho=3, alto=2,
        )
        cls.triaje = Espacio.objects.create(
            institucion=cls.inst, nombre="Triaje", tipo="triaje", x=5, y=1, ancho=2, alto=2,
        )

    def _cita(self, hora, estado, espacio, paciente=None):
        return Cita.objects.create(
            institucion=self.inst,
            paciente=paciente or self.paciente,
            profesional=self.medico,
            fecha=timezone.localdate(),
            hora=hora,
            estado=estado,
            espacio=espacio,
        )

    def test_sala_sin_cita_esta_libre(self):
        plano = estado_plano([self.inst])
        triaje = next(f for f in plano["espacios"] if f["nombre"] == "Triaje")
        self.assertEqual(triaje["estado"], "libre")
        self.assertIsNone(triaje["iniciales"] or None)

    def test_cita_en_espera_marca_esperando_con_minutos(self):
        ahora = timezone.localtime()
        hora = (ahora - timedelta(minutes=25)).time()
        self._cita(hora, "en_espera", self.consulta)
        plano = estado_plano([self.inst])
        sala = next(f for f in plano["espacios"] if f["nombre"] == "Consultorio 1")
        self.assertEqual(sala["estado"], "esperando")
        self.assertGreaterEqual(sala["minutos"], 24)
        self.assertTrue(sala["critico"])
        self.assertEqual(sala["iniciales"], "AP")

    def test_cita_futura_es_reservado(self):
        hora = (timezone.localtime() + timedelta(minutes=40)).time()
        self._cita(hora, "confirmada", self.triaje)
        plano = estado_plano([self.inst])
        sala = next(f for f in plano["espacios"] if f["nombre"] == "Triaje")
        self.assertEqual(sala["estado"], "reservado")
        self.assertGreater(sala["minutos_para"], 0)

    def test_cita_atendida_marca_atendida(self):
        self._cita(time(8, 0), "atendida", self.consulta)
        plano = estado_plano([self.inst])
        sala = next(f for f in plano["espacios"] if f["nombre"] == "Consultorio 1")
        self.assertEqual(sala["estado"], "atendida")

    def test_resumen_y_citas_sin_sala(self):
        self._cita(time(9, 0), "en_espera", self.consulta)
        self._cita(time(9, 30), "confirmada", None)
        plano = estado_plano([self.inst])
        self.assertEqual(plano["total"], 2)
        self.assertEqual(plano["esperando"], 1)
        self.assertEqual(plano["sin_sala"], 1)
        self.assertEqual([f["nombre"] for f in plano["por_espera"]], ["Consultorio 1"])

    def test_dimensiones_del_plano(self):
        plano = estado_plano([self.inst])
        self.assertGreaterEqual(plano["columnas"], 7)  # 5 + 2 del triaje
        self.assertGreaterEqual(plano["filas"], 3)  # 1 + 2 del consultorio


class PlanoVistaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inst = Institucion.objects.create(nombre="Clinica Plano", subdominio="plano")
        cls.esp = Especialidad.objects.create(nombre="Medicina General", nivel="primero", institucion=cls.inst)
        cls.admin_user = User.objects.create_user("adm", password="x")
        Profesional.objects.create(
            usuario=cls.admin_user, nombre="Ana Admin", tipo="admin",
            especialidad=cls.esp, institucion=cls.inst, activo=True,
        )
        cls.medico_user = User.objects.create_user("med", password="x")
        Profesional.objects.create(
            usuario=cls.medico_user, nombre="Dr. Med", tipo="medico",
            especialidad=cls.esp, institucion=cls.inst, activo=True,
        )
        Espacio.objects.create(institucion=cls.inst, nombre="Consultorio 1", x=1, y=1)

    def test_admin_ve_el_plano(self):
        self.client.force_login(self.admin_user)
        r = self.client.get(reverse("dashboards_plano"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Plano de la clínica")
        self.assertContains(r, "Consultorio 1")

    def test_medico_no_ve_el_plano(self):
        self.client.force_login(self.medico_user)
        r = self.client.get(reverse("dashboards_plano"))
        self.assertEqual(r.status_code, 302)


class PlanoAccionesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inst = Institucion.objects.create(nombre="Clinica Acciones", subdominio="acciones")
        cls.esp = Especialidad.objects.create(nombre="Medicina General", nivel="primero", institucion=cls.inst)
        cls.recep_user = User.objects.create_user("rec", password="x")
        Profesional.objects.create(
            usuario=cls.recep_user, nombre="Rita Recepción", tipo="recepcionista",
            especialidad=cls.esp, institucion=cls.inst, activo=True,
        )
        cls.medico_user = User.objects.create_user("med2", password="x")
        cls.medico = Profesional.objects.create(
            usuario=cls.medico_user, nombre="Dr. Dos", tipo="medico",
            especialidad=cls.esp, institucion=cls.inst, activo=True,
        )
        cls.sala = Espacio.objects.create(institucion=cls.inst, nombre="Consultorio A", x=1, y=1)
        cls.paciente = Paciente.objects.create(
            nombre="Luis", apellido="Paz", documento="9", institucion=cls.inst, activo=True,
        )
        cls.cita = Cita.objects.create(
            institucion=cls.inst, paciente=cls.paciente, profesional=cls.medico,
            fecha=timezone.localdate(), hora=time(9, 0), estado="confirmada",
        )

    def test_asignar_sala(self):
        self.client.force_login(self.recep_user)
        r = self.client.post(
            reverse("dashboards_plano_asignar"),
            {"cita": self.cita.id, "espacio": self.sala.id},
        )
        self.assertEqual(r.status_code, 302)
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.espacio, self.sala)

    def test_marcar_llegada(self):
        self.client.force_login(self.recep_user)
        r = self.client.post(reverse("dashboards_plano_llegada"), {"cita": self.cita.id})
        self.assertEqual(r.status_code, 302)
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.estado, "en_espera")

    def test_liberar_sala(self):
        self.cita.espacio = self.sala
        self.cita.save(update_fields=["espacio"])
        self.client.force_login(self.recep_user)
        r = self.client.post(reverse("dashboards_plano_liberar"), {"cita": self.cita.id})
        self.assertEqual(r.status_code, 302)
        self.cita.refresh_from_db()
        self.assertIsNone(self.cita.espacio)

    def test_medico_no_puede_operar(self):
        self.client.force_login(self.medico_user)
        r = self.client.post(
            reverse("dashboards_plano_asignar"),
            {"cita": self.cita.id, "espacio": self.sala.id},
        )
        self.assertIn(r.status_code, (302, 403))
        self.cita.refresh_from_db()
        self.assertIsNone(self.cita.espacio)

    def test_solo_post(self):
        self.client.force_login(self.recep_user)
        r = self.client.get(reverse("dashboards_plano_asignar"))
        self.assertEqual(r.status_code, 405)
