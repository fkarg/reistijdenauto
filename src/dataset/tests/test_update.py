import os

from django.test import TestCase

from django.conf import settings
from dataset.models import WegStuk
from dataset.update import _parse_and_store_geojson
from django.contrib.gis.utils.layermapping import LayerMapError

_GOOD_GEOJSON = os.path.join(settings.TESTDATA_DIR, 'reistijdenAmsterdam.geojson')
_BAD_GEOJSON = os.path.join(settings.TESTDATA_DIR, 'bad_missing_attribute.geojson')


class UpdateTestCase(TestCase):
    def test_geojson_parsing_good_data(self):
        _parse_and_store_geojson(_GOOD_GEOJSON)

        # We know the number of road stretches in data:
        self.assertEqual(len(WegStuk.objects.all()), 1012)

        example = WegStuk.objects.get(id='RWS01_MONIBAS_0091hrl0356ra0')
        self.assertIsInstance(example, WegStuk)

    def test_geojson_parsing_bad_data(self):
        with self.assertRaises(LayerMapError):
            _parse_and_store_geojson(_BAD_GEOJSON)
