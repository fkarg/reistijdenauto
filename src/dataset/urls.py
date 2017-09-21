from django.conf.urls import url, include
from rest_framework import routers

from .views import WegStukViewSet

router = routers.DefaultRouter()
router.register(r'wegstuk', WegStukViewSet)
urlpatterns = router.urls
