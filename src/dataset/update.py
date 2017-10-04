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


REISTIJDEN_TARGET_URL = 'http://web.redant.net/~amsterdam/ndw/data/reistijdenAmsterdam.geojson'  # noqa
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
TEMP_DOWNLOAD_DIR = os.path.join('/', 'tmp')


class SanityCheckError(Exception):
    pass


def download_and_update():
    """
    Download Reistijden GeoJSON and save it to the database.
    """
    with tempfile.TemporaryDirectory(dir=TEMP_DOWNLOAD_DIR) as temp_dir:
        reistijden_jsonfile = os.path.join(temp_dir, 'reistijdenAmsterdam.geojson')

        r = requests.get(REISTIJDEN_TARGET_URL)
        with open(reistijden_jsonfile, 'w') as f:
            f.write(r.text)

        _parse_and_store_geojson(reistijden_jsonfile)


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
