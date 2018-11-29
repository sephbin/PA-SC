from django.urls import path
from . import views

app_name = 'tests'
urlpatterns = [
    path(r'ortho', views.ortho),
    path(r'dir', views.dir),
]