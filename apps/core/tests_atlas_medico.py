from unittest import mock

from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase

from apps.core.atlas_catalog import module_by_id, modules_for_hub
from apps.core.atlas_explore import agenda_exploracion
from apps.core.atlas_ui import resolve_atlas_iso_scene


class MedicoHubCatalogTests(SimpleTestCase):
    """Catálogo del hub del médico y filtrado por permisos."""

    def _user(self):
        return type("U", (), {"is_authenticated": True, "is_superuser": False})()

    def test_area_medico_devuelve_los_tres_modulos(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=True):
            ids = [m.id for m in modules_for_hub(self._user(), area="medico")]
        self.assertEqual(ids, ["agenda_medico", "espera_medico", "historia_medico"])

    def test_area_medico_sin_permiso_de_pacientes_oculta_historia(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=False):
            ids = [m.id for m in modules_for_hub(self._user(), area="medico")]
        self.assertEqual(ids, ["agenda_medico", "espera_medico"])

    def test_area_recepcion_no_cambia(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=True):
            ids = [m.id for m in modules_for_hub(self._user())]
        self.assertEqual(ids, ["pacientes", "citas", "flujo_dia"])

    def test_module_by_id_respeta_el_area(self):
        self.assertIsNotNone(module_by_id("historia_medico", area="medico"))
        self.assertIsNone(module_by_id("historia_medico", area="recepcion"))
        self.assertIsNotNone(module_by_id("pacientes"))

    def test_todos_los_modulos_tienen_assets_cerrado_y_abierto(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=True):
            modulos = modules_for_hub(self._user(), area="medico")
        for modulo in modulos:
            self.assertTrue(modulo.asset_closed.endswith(".webp"))
            self.assertTrue(modulo.asset_open.endswith(".webp"))


class MedicoHubTemplateTests(SimpleTestCase):
    """El hub del médico renderiza objetos accesibles y un panel por módulo."""

    def _context(self):
        with mock.patch("apps.core.atlas_catalog.can_view_pacientes", return_value=True):
            modules = modules_for_hub(type("U", (), {"is_authenticated": True})(), area="medico")
        return {
            "interface_mode": "atlas",
            "atlas_interactive": True,
            "atlas_iso_scene": "medico",
            "atlas_modules": modules,
            "agenda_explore": {
                "hoy_total": 6,
                "atendidas": 2,
                "por_atender": 4,
                "proxima_hora": None,
                "fecha": None,
                "por_estado": [
                    {"code": "pendiente", "label": "Pendiente", "total": 3, "pct": 100},
                    {"code": "atendida", "label": "Atendida", "total": 2, "pct": 67},
                ],
            },
            "espera_explore": {
                "en_espera": 4,
                "listos": 3,
                "sin_signos": 1,
                "espera_media": 12,
                "espera_maxima": 40,
                "tope_espera": 30,
            },
            "historia_explore": {
                "consultas_hoy": 2,
                "consultas_30d": 18,
                "total_diagnosticos": 21,
                "top_diagnosticos": [
                    {"nombre": "Hipertensión", "total": 5, "pct": 100},
                ],
            },
        }

    def test_hub_renderiza_tres_objetos_y_tres_paneles(self):
        html = render_to_string("atlas/hub_medico.html", self._context())
        self.assertEqual(html.count('data-atlas-module="'), 3)
        self.assertEqual(html.count("data-atlas-panel="), 3)
        self.assertIn('data-atlas-module="agenda_medico"', html)
        self.assertIn('data-atlas-module="espera_medico"', html)
        self.assertIn('data-atlas-module="historia_medico"', html)

    def test_objetos_son_botones_con_aria_controls(self):
        html = render_to_string("atlas/hub_medico.html", self._context())
        self.assertEqual(html.count("<button"), 3)
        self.assertEqual(html.count('aria-controls="xm-atlas-explore-medico"'), 3)

    def test_paneles_empiezan_ocultos(self):
        html = render_to_string("atlas/hub_medico.html", self._context())
        self.assertIn('data-atlas-explore hidden', html)
        self.assertEqual(html.count('class="xm-atlas-explore__panel" data-atlas-panel='), 3)

    def test_panel_de_espera_muestra_umbral_y_datos(self):
        html = render_to_string("atlas/explore_espera_medico.html", {"explore": self._context()["espera_explore"]})
        self.assertIn("40 min", html)
        self.assertIn("umbral de referencia", html.lower())
        self.assertIn("width: 133%", html)


class MedicoSceneTests(SimpleTestCase):
    def test_dashboard_resuelve_escena_medico(self):
        request = RequestFactory().get("/")
        request.resolver_match = type("M", (), {"url_name": "dashboard"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "medico")


class AgendaMedicoAggregatesTests(SimpleTestCase):
    """La agregación no expone identidad de pacientes (sólo conteos)."""

    def test_claves_del_resumen(self):
        import inspect

        source = inspect.getsource(agenda_exploracion)
        for prohibido in ("nombre", "apellido", "paciente.nombre"):
            self.assertNotIn(prohibido, source)
