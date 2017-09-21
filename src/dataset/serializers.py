from rest_framework import serializers
from rest_framework_gis.serializers import GeometrySerializerMethodField
from rest_framework_gis.fields import GeometryField
from .models import WegStuk


class WegStukSerializer(serializers.HyperlinkedModelSerializer):
    mline = GeometryField()

    class Meta:
        model = WegStuk
        fields = (
            '_id', 'name', '_type', 'timestamp', 'length', 'traveltime',
            'velocity', 'mline')
