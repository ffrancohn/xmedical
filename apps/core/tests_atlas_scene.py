from django.template.loader import render_to_string
from django.test import SimpleTestCase

from apps.core.atlas_scene import construir_escena_especialista, construir_escena_medico

AGENDA = {
    "hoy_total": 5,
    "atendidas": 2,
    "por_atender": 3,
    "proxima_hora": None,
    "por_estado": [
        {"code": "pendiente", "label": "Pendiente", "total": 1},
        {"code": "atendida", "label": "Atendida", "total": 2},
    ],
    "fecha": None,
}
ESPERA = {
    "en_espera": 3,
    "listos": 1,
    "sin_signos": 2,
    "espera_media": 12,
    "espera_maxima": 20,
    "tope_espera": 30,
}
HISTORIA = {
    "consultas_hoy": 2,
    "consultas_30d": 18,
    "total_diagnosticos": 21,
    "top_diagnosticos": [{"nombre": "Hipertensión arterial", "total": 5, "pct": 100}],
    "desde": None,
}
REFS = {
    "pendientes": 4,
    "aceptadas": 1,
    "completadas": 2,
    "espera_media_dias": 2.4,
    "por_prioridad": [
        {"code": "alta", "label": "Alta", "total": 2},
        {"code": "media", "label": "Media", "total": 1},
        {"code": "baja", "label": "Baja", "total": 1},
    ],
    "por_especialidad": [{"especialidad_destino__nombre": "Cardiología", "total": 2}],
}
URLS = {
    "citas": "/citas/",
    "preclinica": "/preclinica/",
    "pacientes": "/pacientes/",
    "epidemiologia": "/dashboards/epidemiologia/",
}


class EscenaMedicoPayloadTests(SimpleTestCase):
    def _payload(self):
        return construir_escena_medico(
            AGENDA, ESPERA, HISTORIA, URLS, perfil="Dr. Test", especialidad="Medicina General"
        )

    def test_tres_estaciones_con_panel(self):
        ids = [e["id"] for e in self._payload()["estaciones"]]
        self.assertEqual(ids, ["agenda", "espera", "historia"])

    def test_kpis_reflejan_los_agregados(self):
        agenda = self._payload()["estaciones"][0]
        valores = {k["etiqueta"]: k["valor"] for k in agenda["kpis"]}
        self.assertEqual(valores["Citas"], 5)
        self.assertEqual(valores["Atendidas"], 2)
        self.assertEqual(valores["Siguiente"], "\u2014")

    def test_barras_traen_porcentaje(self):
        barras = self._payload()["estaciones"][1]["barras"]
        self.assertTrue(all(0 <= b["pct"] <= 100 for b in barras))
        # 2 sin signos y 1 listo sobre 3 en espera
        self.assertEqual([b["pct"] for b in barras], [67, 33])

    def test_acciones_apuntan_a_urls_reales(self):
        acciones = self._payload()["estaciones"][0]["acciones"]
        self.assertEqual(acciones[0]["url"], "/citas/")

    def test_paciente_en_silla_refleja_la_espera(self):
        paciente = self._payload()["paciente"]
        self.assertTrue(paciente["ocupada"])
        self.assertEqual(paciente["total"], 3)

    def test_aria_lleva_el_dato(self):
        aria = self._payload()["estaciones"][1]["aria"]
        self.assertIn("3 pacientes", aria)

    def test_sin_nombres_de_pacientes(self):
        texto = str(self._payload())
        self.assertNotIn("Rosa", texto)
        self.assertNotIn("apellido", texto)


class EscenaMedicoTemplateTests(SimpleTestCase):
    def test_renderiza_escena_json_y_tabla(self):
        payload = construir_escena_medico(AGENDA, ESPERA, HISTORIA, URLS, perfil="Dr. Test")
        html = render_to_string("atlas/scene.html", {"atlas_scene": payload})

        self.assertIn('id="xm-scene-svg"', html)
        self.assertIn('id="xm-scene-data"', html)
        self.assertIn('id="xm-scene-panel"', html)
        self.assertIn('id="xm-scene-table"', html)
        self.assertEqual(html.count("<tr>"), 1 + 3)  # cabecera + 3 estaciones
        self.assertIn("Agenda de hoy", html)
        self.assertIn("Dr. Test", html)

    def test_tabla_es_el_fallback_con_las_acciones(self):
        payload = construir_escena_medico(AGENDA, ESPERA, HISTORIA, URLS)
        html = render_to_string("atlas/scene.html", {"atlas_scene": payload})
        self.assertIn('href="/citas/"', html)
        self.assertIn("Vista de tabla (equivalente)", html)


class EscenaEspecialistaTests(SimpleTestCase):
    def _payload(self):
        return construir_escena_especialista(
            AGENDA,
            ESPERA,
            REFS,
            dict(URLS, referencias="/referencias/"),
            perfil="Dra. Test",
            especialidad="Cardiología",
        )

    def test_la_bandeja_sustituye_al_archivo(self):
        ids = [e["id"] for e in self._payload()["estaciones"]]
        self.assertEqual(ids, ["agenda", "espera", "derivaciones"])

    def test_kpis_de_referencias(self):
        est = self._payload()["estaciones"][2]
        valores = {k["etiqueta"]: k["valor"] for k in est["kpis"]}
        self.assertEqual(valores["Pendientes"], 4)
        self.assertEqual(valores["Espera media"], "2.4 d")

    def test_acciones_apuntan_a_referencias(self):
        acciones = self._payload()["estaciones"][2]["acciones"]
        self.assertEqual(acciones[0]["url"], "/referencias/")

    def test_aria_de_derivaciones(self):
        self.assertIn("4 pendientes", self._payload()["estaciones"][2]["aria"])

    def test_renderiza_panel_de_derivaciones(self):
        html = render_to_string("atlas/scene.html", {"atlas_scene": self._payload()})
        self.assertIn("Derivaciones", html)
        self.assertIn('href="/referencias/"', html)
        self.assertEqual(html.count("<tr>"), 4)
