from drf_hal_json.serializers import HalModelSerializer
from rest_framework_gis.fields import GeometryField
from .models import WegStuk


class WegStukSerializer(HalModelSerializer):
    mline = GeometryField()
    # 'URL_FIELD_NAME': 'self'  (should be set in REST_FRAMEWORK settings dict)

    class Meta:
        model = WegStuk
        fields = (
            'id', 'name', 'type', 'timestamp', 'length', 'traveltime',
            'velocity', 'mline')
