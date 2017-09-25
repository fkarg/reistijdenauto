#  INFO: Open of `reistijdenAmsterdam.geojson'
#        using driver `GeoJSON' successful.
#
#  Layer name: reistijdenAmsterdam
#  Geometry: Line String
#  Feature Count: 1012
#  Extent: (4.704348, 52.246392) - (5.177359, 52.475149)
#  Layer SRS WKT:
#  GEOGCS["WGS 84",
#      DATUM["WGS_1984",
#          SPHEROID["WGS 84",6378137,298.257223563,
#              AUTHORITY["EPSG","7030"]],
#          AUTHORITY["EPSG","6326"]],
#      PRIMEM["Greenwich",0,
#          AUTHORITY["EPSG","8901"]],
#      UNIT["degree",0.0174532925199433,
#          AUTHORITY["EPSG","9122"]],
#      AUTHORITY["EPSG","4326"]]
#  Id: String (0.0)
#  Name: String (0.0)
#  Type: String (0.0)
#  Timestamp: DateTime (0.0)
#  Length: Integer (0.0)
#  Traveltime: Integer (0.0)
#  Velocity: Integer (0.0)

from django.contrib.gis.db import models


class WegStuk(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(max_length=255)   # convert to datetime
    length = models.IntegerField()
    traveltime = models.IntegerField()
    velocity = models.IntegerField()

    mline = models.LineStringField()

    def __str__(self):
        return self.name
