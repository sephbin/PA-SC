from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register(r'characters', views.CharacterViewSet)

app_name = 'scrpgtest'
urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path(r'', views.home),
    # path(r'card/<int:characterid>/', views.card),
    # path(r'character/<int:characterid>/', views.characterdata),
    # path(r'characterlist/', views.characterlist),
]