from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

# router = routers.DefaultRouter()
# router.register(r'characters', views.CharacterViewSet)

urlpatterns = [
	path(r'', views.index),
	path(r'<path:path>', views.index),


]