from django.conf.urls import url, include

urlpatterns = [
    url(r'^reistijdenauto/', include('dataset.urls'))
]
