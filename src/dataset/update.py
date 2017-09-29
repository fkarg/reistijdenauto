import os
import tempfile
import logging

import requests
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from dataset.models import WegStuk


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


TARGET = 'http://web.redant.net/~amsterdam/ndw/data/reistijdenAmsterdam.geojson'
MAPPING = {
    'id': 'Id',
    'name': 'Name',
    'type': 'Type',
    'timestamp': 'Timestamp',
    'length': 'Length',
    'traveltime': 'Traveltime',
    'velocity': 'Velocity',
    'mline': 'LINESTRING'
}


class SanityCheckError(Exception):
    pass


def download_and_update():
    """
    Download Reistijden GeoJSON and save it to the database.
    """
    with tempfile.TemporaryDirectory(dir='/tmp') as temp_dir:
        # TODO: research interactions of /tmp temporary directories and
        # container file system LOOK FOR: --mount type=tempfs ...
        temp_file = os.path.join(temp_dir, 'reistijdenAmsterdam.geojson')

        r = requests.get(TARGET)
        with open(temp_file, 'w') as f:
            f.write(r.text)

        _parse_and_store_geojson(temp_file)


def _parse_and_store_geojson(filename):
    """Parse source GeoJSON with travel times."""
    ds = DataSource(filename)
    _sanity_check_datasource(ds)

    logger.info('Data file %s was opened', ds.name)
    lm = LayerMapping(WegStuk, ds, MAPPING)

    with transaction.atomic():
        WegStuk.objects.all().delete()
        lm.save(strict=True, verbose=False)

    logger.info('Travel time dataset was updated.')


def _sanity_check_datasource(ds):
    """
    Hardcoded sanity checks, assumes input GeoJSON does not change.
    """
    if len(ds) != 1:
        raise SanityCheckError('GeoJSON should have only 1 layer.')
    # TODO: add more checks
