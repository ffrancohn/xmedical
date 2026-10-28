from django.test import RequestFactory, SimpleTestCase

from apps.core.atlas_ui import resolve_atlas_iso_scene


class ResolveAtlasIsoSceneTests(SimpleTestCase):
    def test_ruta_recepcion(self):
        request = RequestFactory().get("/dashboards/recepcion/")
        request.resolver_match = type("M", (), {"url_name": "dashboards_recepcion"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "recepcion")

    def test_default_clinic(self):
        request = RequestFactory().get("/pacientes/")
        request.resolver_match = type("M", (), {"url_name": "pacientes_lista"})()
        request.user = type("U", (), {"is_authenticated": False})()
        self.assertEqual(resolve_atlas_iso_scene(request), "clinic")
