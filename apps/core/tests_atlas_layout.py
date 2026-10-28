from django.test import RequestFactory, SimpleTestCase

from apps.core.atlas_layout import atlas_stage_context, atlas_stage_enabled


class _Pref:
    interface_mode = "atlas"


class _User:
    is_authenticated = True
    preference = _Pref()


class AtlasStageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = _User()

    def test_atlas_stage_enabled(self):
        request = self.factory.get("/pacientes/nuevo/")
        request.user = self.user
        self.assertTrue(atlas_stage_enabled(request))
        request = self.factory.get("/pacientes/nuevo/", {"classic": "1"})
        request.user = self.user
        self.assertFalse(atlas_stage_enabled(request))

    def test_atlas_stage_context_includes_copy(self):
        request = self.factory.get("/citas/agendar/")
        request.user = self.user
        ctx = atlas_stage_context(request, "citas", title="Agendar", lead="Texto guía")
        self.assertTrue(ctx["atlas_stage"])
        self.assertEqual(ctx["atlas_stage_title"], "Agendar")
        self.assertIn("ver=agenda", ctx["atlas_stage_back_url"])
