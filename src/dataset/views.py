from rest_framework import viewsets
from .serializers import WegStukSerializer
from .models import WegStuk


class WegStukViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WegStukSerializer
    queryset = WegStuk.objects.all().order_by('id')
