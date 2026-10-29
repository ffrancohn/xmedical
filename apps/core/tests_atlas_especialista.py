from unittest import mock

from django.template.loader import render_to_string
from django.test import SimpleTestCase

from apps.core.atlas_catalog import module_by_id, modules_for_hub
from apps.core.atlas_explore import referencias_exploracion


class EspecialistaHubCatalogTests(SimpleTestCase):
    def _user(self):
        return type("U", (), {"is_authenticated": True, "is_superuser": False})()

    def test_area_especialista_devuelve_los_tres_modulos(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=True):
            ids = [m.id for m in modules_for_hub(self._user(), area="especialista")]
        self.assertEqual(ids, ["agenda_especialista", "espera_especialista", "derivaciones"])

    def test_sin_permiso_de_pacientes_oculta_derivaciones(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=False):
            ids = [m.id for m in modules_for_hub(self._user(), area="especialista")]
        self.assertEqual(ids, ["agenda_especialista", "espera_especialista"])

    def test_areas_no_se_mezclan(self):
        self.assertIsNotNone(module_by_id("derivaciones", area="especialista"))
        self.assertIsNone(module_by_id("derivaciones", area="medico"))
        self.assertIsNone(module_by_id("agenda_medico", area="especialista"))

    def test_assets_de_derivaciones_existen_en_el_paquete(self):
        modulo = module_by_id("derivaciones", area="especialista")
        self.assertEqual(modulo.asset_closed, "atlas-interactive/assets/v1/modulos/consultas.webp")
        self.assertEqual(modulo.asset_open, "atlas-interactive/assets/v1/modulos/diagnostico.webp")


class EspecialistaHubTemplateTests(SimpleTestCase):
    def _context(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=True):
            modules = modules_for_hub(type("U", (), {"is_authenticated": True})(), area="especialista")
        return {
            "interface_mode": "atlas",
            "atlas_interactive": True,
            "atlas_iso_scene": "especialista",
            "atlas_modules": modules,
            "agenda_explore": {
                "hoy_total": 4,
                "atendidas": 1,
                "por_atender": 3,
                "proxima_hora": None,
                "fecha": None,
                "por_estado": [{"code": "pendiente", "label": "Pendiente", "total": 3, "pct": 100}],
            },
            "espera_explore": {
                "en_espera": 3,
                "listos": 2,
                "sin_signos": 1,
                "espera_media": 9,
                "espera_maxima": 15,
                "tope_espera": 30,
            },
            "derivaciones_explore": {
                "pendientes": 7,
                "aceptadas": 3,
                "completadas": 5,
                "espera_media_dias": 2.4,
                "por_prioridad": [
                    {"code": "alta", "label": "Alta", "total": 4, "pct": 100},
                    {"code": "media", "label": "Media", "total": 2, "pct": 50},
                ],
                "por_especialidad": [
                    {"especialidad_destino__nombre": "Cardiología", "total": 4},
                ],
            },
        }

    def test_hub_renderiza_tres_objetos_y_tres_paneles(self):
        html = render_to_string("atlas/hub_especialista.html", self._context())
        self.assertEqual(html.count('data-atlas-module="'), 3)
        self.assertEqual(html.count("data-atlas-panel="), 3)
        self.assertIn('data-atlas-module="derivaciones"', html)
        self.assertEqual(html.count('aria-controls="xm-atlas-explore-especialista"'), 3)

    def test_panel_de_derivaciones_muestra_prioridades_y_espera(self):
        html = render_to_string(
            "atlas/explore_derivaciones.html", {"explore": self._context()["derivaciones_explore"]}
        )
        self.assertIn("Derivaciones — tu bandeja", html)
        # El separador decimal depende del locale activo (es: 2,4 / en: 2.4).
        self.assertRegex(html, r"2[.,]4")
        self.assertIn("Cardiología", html)
        self.assertEqual(html.count("xm-atlas-bar__fill"), 2)

    def test_prioridad_alta_usa_la_barra_de_alerta(self):
        html = render_to_string(
            "atlas/explore_derivaciones.html", {"explore": self._context()["derivaciones_explore"]}
        )
        self.assertIn('class="xm-atlas-bar xm-atlas-bar--wait"', html)
        self.assertIn("de 7 pendientes", html)

    def test_barras_tienen_etiqueta_accesible(self):
        html = render_to_string(
            "atlas/explore_derivaciones.html", {"explore": self._context()["derivaciones_explore"]}
        )
        self.assertEqual(html.count('role="img"'), 2)
        self.assertEqual(html.count("aria-label="), 2)


class DerivacionesAggregatesTests(SimpleTestCase):
    def test_la_agregacion_no_expone_identidad_de_pacientes(self):
        import inspect

        source = inspect.getsource(referencias_exploracion)
        self.assertNotIn("paciente", source.lower())
        self.assertNotIn("diagnostico", source.lower())
