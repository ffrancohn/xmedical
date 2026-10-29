from datetime import date

from django.test import SimpleTestCase

from apps.core.atlas_explore import (
    DEFAULT_AGE_BUCKETS,
    _age_years,
    _bucket_for_age,
    avatar_static_paths,
    birth_date_range_for_bucket,
    get_age_buckets,
)


class AtlasExploreLogicTests(SimpleTestCase):
    def test_age_buckets_default(self):
        buckets = get_age_buckets(None)
        self.assertEqual(len(buckets), len(DEFAULT_AGE_BUCKETS))

    def test_bucket_for_age(self):
        buckets = get_age_buckets(None)
        self.assertEqual(_bucket_for_age(8, buckets), "ninos")
        self.assertEqual(_bucket_for_age(25, buckets), "adultos_jovenes")
        self.assertEqual(_bucket_for_age(None, buckets), "sin_edad")

    def test_birth_date_range_adultos(self):
        on = date(2026, 6, 15)
        buckets = get_age_buckets(None)
        start, end = birth_date_range_for_bucket("adultos", buckets, on_date=on)
        self.assertIsNotNone(start)
        self.assertIsNotNone(end)
        age = _age_years(date(1980, 3, 1), on)
        self.assertGreaterEqual(age, 30)
        self.assertLessEqual(age, 59)


class AvatarAssetsTests(SimpleTestCase):
    """El paquete v2 usa `<grupo>_<sexo>.webp`; el prefijo no debe colisionar."""

    def test_adultos_no_captura_adultos_jovenes(self):
        rutas = avatar_static_paths("adultos", limit=10)
        self.assertTrue(rutas)
        for ruta in rutas:
            nombre = ruta.rsplit("/", 1)[-1]
            self.assertTrue(nombre.startswith("adultos_") and not nombre.startswith("adultos_jovenes_"), nombre)

    def test_cada_grupo_tiene_al_menos_un_avatar(self):
        for grupo in ("ninos", "adolescentes", "adultos_jovenes", "adultos", "mayores"):
            with self.subTest(grupo=grupo):
                rutas = avatar_static_paths(grupo, limit=4)
                self.assertTrue(rutas, f"sin avatares para {grupo}")
                self.assertLessEqual(len(rutas), 4)

    def test_archivos_existen_en_disco(self):
        from pathlib import Path

        from django.conf import settings

        base = Path(settings.BASE_DIR) / "static"
        for ruta in avatar_static_paths("ninos", limit=4):
            self.assertTrue((base / ruta).exists(), ruta)
