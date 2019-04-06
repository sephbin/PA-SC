from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path(r'', views.home),
    path(r'temp', views.temp),
]