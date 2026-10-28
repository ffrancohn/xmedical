from datetime import date

from django.test import SimpleTestCase

from apps.core.atlas_explore import (
    DEFAULT_AGE_BUCKETS,
    _age_years,
    _bucket_for_age,
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
