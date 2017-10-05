from rest_framework_gis.fields import GeometryField

from .models import WegStuk
from .rest import HALSerializer, DisplayField


class WegStukSerializer(HALSerializer):
    mline = GeometryField()
    _display = DisplayField()

    class Meta:
        model = WegStuk
        fields = ('id', 'name', 'type', 'timestamp', 'length', 'traveltime',
                  'velocity', 'mline', '_links', '_display')
