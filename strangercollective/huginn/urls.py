from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'parameters', views.ParameterViewSet)

urlpatterns = [
    path(r'family/<str:familyname>/<str:scripttype>', views.familygetscript),
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rpgapi')),
]