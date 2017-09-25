import tempfile
import os

import requests

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from django.db import transaction


from dataset.models import WegStuk


TARGET = 'http://web.redant.net/~amsterdam/ndw/data/reistijdenAmsterdam.geojson'

mapping = {
    'id': 'Id',
    'name': 'Name',
    'type': 'Type',
    'timestamp': 'Timestamp',
    'length': 'Length',
    'traveltime': 'Traveltime',
    'velocity': 'Velocity',
    'mline': 'LINESTRING'
}


class Command(BaseCommand):
    help = 'Retrieve a new reistijden GeoJSON and store in the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Downloaded GeoJSON'))

        # TODO: research interactions of /tmp temporary directories and
        # container file system LOOK FOR: --mount type=tempfs ...

        self._download_geojson_and_store()

        self.stdout.write(self.style.SUCCESS(
            WegStuk.objects.count()
        ))

    def _download_geojson_and_store(self):
        """
        Download Reistijden GeoJSON and save it to the database.
        """
        with tempfile.TemporaryDirectory(dir='/tmp') as temp_dir:
            temp_file = os.path.join(temp_dir, 'reistijdenAmsterdam.geojson')

            r = requests.get(TARGET)
            with open(temp_file, 'w') as f:
                f.write(r.text)

            ds = DataSource(temp_file)
            self._sanity_check_datasource(ds)

            self.stdout.write(self.style.SUCCESS(
                'Datasource {} was opened'.format(ds.name)))

            lm = LayerMapping(WegStuk, ds, mapping)

            with transaction.atomic():
                WegStuk.objects.all().delete()
                lm.save(strict=True, verbose=False)

    def _sanity_check_datasource(self, ds):
        """
        Hardcoded sanity checks, assumes inputs do not change.
        """
        if len(ds) != 1:
            raise CommandError('GeoJSON should have only 1 layer.')
        # TODO: add more checks
