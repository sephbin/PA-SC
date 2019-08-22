from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

urlpatterns = [
	path(r'clock', views.clock),
]