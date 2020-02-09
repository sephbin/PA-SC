from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'parameters', views.ParameterViewSet)
router.register(r'testmodelser', views.TestViewSet)

urlpatterns = [
    path(r'family/<str:familyname>/<str:scripttype>', views.familygetscript),
    path(r'test/', views.test),
    path(r'upcrparam/', views.create_update_parameter),
    path(r'upcrmap/', views.create_update_map),
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rpgapi')),
]