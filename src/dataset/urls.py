from django.conf.urls import url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .views import WegStukViewSet

schema_view = get_swagger_view('Reistijden auto API')

router = routers.DefaultRouter()
router.register(r'wegstuk', WegStukViewSet)
urlpatterns = router.urls

urlpatterns += [
    url(r'^docs/api-docs/reistijdenauto/', schema_view)
]
