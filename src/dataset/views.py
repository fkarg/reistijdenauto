from .serializers import WegStukSerializer
from .models import WegStuk
from .rest import DatapuntViewSet


class WegStukViewSet(DatapuntViewSet):
    serializer_class = WegStukSerializer
    serializer_detail_class = WegStukSerializer
    queryset = WegStuk.objects.all().order_by('id')
