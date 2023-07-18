from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
import sys

from . import views
from .models import *

router = routers.DefaultRouter()
# for subclass in parentModel.__subclasses__():
# 	vsName = str(subclass.__name__)+"_viewSet"
# 	vsOb = getattr(sys.modules[__name__], vsName)
# 	router.register(subclass,		vsOb)
router.register(r'test', views.geometry_viewset)
urlpatterns = [
	url(r'^', include(router.urls)),
]