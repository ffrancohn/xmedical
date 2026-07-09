"""Pruebas de variables clinicas por especialidad (Fase 2)."""
from datetime import time

from django.test import TestCase
from django.utils import timezone

from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.core.models import Especialidad, Institucion, Profesional
from apps.core.test_utils import auth_client
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica
from apps.variables_clinicas.forms import build_variables_form, guardar_valores_variables
from apps.variables_clinicas.models import ValorVariableClinica, VariableClinica
from apps.variables_clinicas.services import cita_tiene_variables, variables_para_cita


class VariableClinicaModelTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.especialidad = Especialidad.objects.get(pk=1)

    def test_crear_variable_por_especialidad(self):
        variable = VariableClinica.objects.create(
            institucion=self.institucion,
            especialidad=self.especialidad,
            nombre="Frecuencia cardiaca",
            codigo="fc",
            tipo="numero",
            obligatorio=True,
            orden=1,
        )
        self.assertEqual(str(variable), "Frecuencia cardiaca (Medicina General)")


class VariablesClinicasFormTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.institucion = Institucion.objects.get(pk=1)
        self.especialidad = Especialidad.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(12, 0),
            estado="confirmada",
        )
        self.consulta = Consulta.objects.create(institucion=self.institucion, cita=self.cita)
        self.variable_obligatoria = VariableClinica.objects.create(
            institucion=self.institucion,
            especialidad=self.especialidad,
            nombre="Saturacion O2",
            codigo="spo2",
            tipo="numero",
            obligatorio=True,
        )
        self.variable_opcional = VariableClinica.objects.create(
            institucion=self.institucion,
            especialidad=self.especialidad,
            nombre="Observaciones",
            codigo="obs",
            tipo="texto",
            obligatorio=False,
        )

    def test_formulario_valida_campos_obligatorios(self):
        variables = [self.variable_obligatoria, self.variable_opcional]
        form = build_variables_form(
            variables,
            self.consulta,
            {
                f"var_{self.variable_obligatoria.pk}": "",
                f"var_{self.variable_opcional.pk}": "Sin hallazgos",
            },
        )
        self.assertFalse(form.is_valid())

    def test_guardar_valores_por_consulta(self):
        variables = [self.variable_obligatoria, self.variable_opcional]
        form = build_variables_form(
            variables,
            self.consulta,
            {f"var_{self.variable_obligatoria.pk}": "98", f"var_{self.variable_opcional.pk}": "Normal"},
        )
        self.assertTrue(form.is_valid())
        guardar_valores_variables(self.consulta, variables, form.cleaned_data)
        self.assertEqual(ValorVariableClinica.objects.filter(consulta=self.consulta).count(), 2)
        valor = ValorVariableClinica.objects.get(consulta=self.consulta, variable=self.variable_obligatoria)
        self.assertEqual(valor.valor, "98")


class VariablesClinicasWizardTests(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = auth_client("medico.demo")
        self.institucion = Institucion.objects.get(pk=1)
        self.especialidad = Especialidad.objects.get(pk=1)
        self.cita = Cita.objects.create(
            institucion=self.institucion,
            paciente=Paciente.objects.filter(institucion=self.institucion).first(),
            profesional=Profesional.objects.get(pk=2),
            fecha=timezone.localdate(),
            hora=time(13, 0),
            estado="confirmada",
        )
        Preclinica.objects.create(
            institucion=self.institucion,
            cita=self.cita,
            presion_arterial_sis=120,
            presion_arterial_dia=80,
            temperatura="36.5",
        )
        self.variable = VariableClinica.objects.create(
            institucion=self.institucion,
            especialidad=self.especialidad,
            nombre="Glucosa capilar",
            codigo="glucosa",
            tipo="numero",
            obligatorio=True,
        )

    def test_salta_paso_variables_si_no_hay_configuracion(self):
        self.variable.delete()
        Consulta.objects.create(institucion=self.institucion, cita=self.cita, examen_fisico="Normal")
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/4/",
            {"examen_fisico": "Normal"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/paso/6/", response.url)

    def test_paso5_guarda_variables_clinicas(self):
        Consulta.objects.create(institucion=self.institucion, cita=self.cita, examen_fisico="Normal")
        response = self.client.post(
            f"/consulta/cita/{self.cita.pk}/paso/5/",
            {f"var_{self.variable.pk}": "110"},
            **{"HTTP_HOST": "xmedical.cloud"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/paso/6/", response.url)
        consulta = Consulta.objects.get(cita=self.cita)
        valor = ValorVariableClinica.objects.get(consulta=consulta, variable=self.variable)
        self.assertEqual(valor.valor, "110")

    def test_servicios_filtran_por_especialidad(self):
        self.assertTrue(cita_tiene_variables(self.cita))
        self.assertEqual(variables_para_cita(self.cita).count(), 1)
