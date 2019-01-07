from django.urls import path
from . import views

urlpatterns = [
    path(r'<str:colle>/<str:pano>', views.panoramaview),
]
