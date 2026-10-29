import csv
import io
import os
import tempfile

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.consulta.models import CodigoCie10, normalizar_texto
from apps.consulta.sinonimos import expandir_termino
from apps.core.models import Especialidad, Institucion, Profesional


class NormalizacionTests(SimpleTestCase):
    def test_quita_tildes_y_normaliza(self):
        self.assertEqual(normalizar_texto("Hipertensi\u00f3n  Esencial"), "hipertension esencial")
        self.assertEqual(normalizar_texto("  CES\u00c1REA "), "cesarea")
        self.assertEqual(normalizar_texto(""), "")
        self.assertEqual(normalizar_texto(None), "")

    def test_sinonimos_expanden(self):
        self.assertEqual(expandir_termino("HTA"), ["hta", "hipertension"])
        self.assertEqual(expandir_termino("dm2"), ["dm2", "diabetes mellitus no insulinodependiente"])
        self.assertEqual(expandir_termino("apendicitis"), ["apendicitis"])


class BusquedaCie10Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.institucion = Institucion.objects.create(nombre="Clinica Test", subdominio="test")
        cls.especialidad = Especialidad.objects.create(
            nombre="Medicina General", nivel="primero", institucion=cls.institucion
        )
        cls.user = User.objects.create_user("doc", password="clave-segura")
        Profesional.objects.create(
            usuario=cls.user,
            nombre="Dr. Test",
            tipo="medico",
            especialidad=cls.especialidad,
            institucion=cls.institucion,
            activo=True,
        )
        CodigoCie10.objects.create(
            codigo="I10", descripcion="Hipertensi\u00f3n esencial (primaria)", nivel=2,
            capitulo="I00-I99", bloque="I10-I15",
        )
        CodigoCie10.objects.create(
            codigo="E11", descripcion="Diabetes mellitus no insulinodependiente", nivel=2,
            capitulo="E00-E89", bloque="E10-E14",
        )
        CodigoCie10.objects.create(
            codigo="I00-I99", descripcion="Enfermedades del sistema circulatorio", nivel=0, es_hoja=False,
        )

    def setUp(self):
        self.client.force_login(self.user)
        self.url = reverse("cie10_search")

    def _codes(self, q):
        response = self.client.get(self.url, {"q": q})
        self.assertEqual(response.status_code, 200)
        return [r["codigo"] for r in response.json()["results"]]

    def test_encuentra_con_tilde(self):
        self.assertIn("I10", self._codes("Hipertensi\u00f3n"))

    def test_encuentra_sin_tilde(self):
        self.assertIn("I10", self._codes("hipertension"))

    def test_abreviatura_hta(self):
        self.assertIn("I10", self._codes("HTA"))

    def test_abreviatura_dm2(self):
        self.assertIn("E11", self._codes("DM2"))

    def test_codigo_exacto_primero(self):
        self.assertEqual(self._codes("I10")[0], "I10")

    def test_capitulos_no_salen_en_el_buscador(self):
        self.assertNotIn("I00-I99", self._codes("enfermedades del sistema circulatorio"))

    def test_respuesta_incluye_total_y_flag(self):
        data = self.client.get(self.url, {"q": "diabetes"}).json()
        self.assertTrue(data["catalogo"])
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["results"][0]["nombre"], "Diabetes mellitus no insulinodependiente")


class FallbackTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.institucion = Institucion.objects.create(nombre="Clinica Test", subdominio="test")
        cls.especialidad = Especialidad.objects.create(
            nombre="Medicina General", nivel="primero", institucion=cls.institucion
        )
        cls.user = User.objects.create_user("doc2", password="clave-segura")
        Profesional.objects.create(
            usuario=cls.user, nombre="Dr. Test", tipo="medico",
            especialidad=cls.especialidad, institucion=cls.institucion, activo=True,
        )

    def test_sin_catalogo_usa_lista_mvp(self):
        self.client.force_login(self.user)
        data = self.client.get(reverse("cie10_search"), {"q": "hipertension"}).json()
        self.assertFalse(data["catalogo"])
        self.assertEqual([r["codigo"] for r in data["results"]], ["I10"])


class ImportCommandTests(TestCase):
    def test_importa_csv_jerarquizado(self):
        contenido = (
            "code,code_0,code_1,code_2,code_3,code_4,description,level,source\n"
            "A00-B99,,,,,,Ciertas enfermedades infecciosas y parasitarias,0,test\n"
            "A00,A00-B99,A00-A09,,,,C\u00f3lera,2,test\n"
            "A000,A00-B99,A00-A09,,,,\"C\u00f3lera debida a Vibrio cholerae O1, biotipo cl\u00e1sico\",4,test\n"
        )
        ruta = os.path.join(tempfile.mkdtemp(), "cie.csv")
        with io.open(ruta, "w", encoding="utf-8", newline="") as fh:
            fh.write(contenido)

        call_command("import_cie10", "--csv", ruta, "--truncate", verbosity=0)

        self.assertEqual(CodigoCie10.objects.count(), 3)
        self.assertEqual(CodigoCie10.objects.filter(es_hoja=True).count(), 2)
        colera = CodigoCie10.objects.get(codigo="A00")
        self.assertEqual(colera.capitulo, "A00-B99")
        self.assertEqual(colera.busqueda, "a00 colera")
        capitulo = CodigoCie10.objects.get(codigo="A00-B99")
        self.assertFalse(capitulo.es_hoja)
