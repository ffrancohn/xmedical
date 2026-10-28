from django.test import RequestFactory, SimpleTestCase

from apps.core.atlas_ui import resolve_atlas_iso_scene


class ResolveAtlasIsoSceneTests(SimpleTestCase):
    def test_ruta_recepcion(self):
        request = RequestFactory().get("/dashboards/recepcion/")
        request.resolver_match = type("M", (), {"url_name": "dashboards_recepcion"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "recepcion")

    def test_ruta_pacientes_recepcion(self):
        request = RequestFactory().get("/pacientes/")
        request.resolver_match = type("M", (), {"url_name": "pacientes_lista"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "recepcion")

    def test_ruta_citas_recepcion(self):
        request = RequestFactory().get("/citas/")
        request.resolver_match = type("M", (), {"url_name": "citas_lista"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "recepcion")

    def test_ruta_preclinica_enfermeria(self):
        request = RequestFactory().get("/preclinica/1/")
        request.resolver_match = type("M", (), {"url_name": "preclinica_registro"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "enfermeria")

    def test_ruta_consulta_wizard_medico(self):
        request = RequestFactory().get("/consulta/cita/1/paso/1/")
        request.resolver_match = type("M", (), {"url_name": "consulta_wizard"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "medico")

    def test_ruta_historia_clinica_medico(self):
        request = RequestFactory().get("/consulta/historia/1/")
        request.resolver_match = type("M", (), {"url_name": "historia_clinica"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "medico")
