from django.urls import path
from . import views

urlpatterns = [
    path(r'<str:collection>/<str:pano>', views.panoramaview),
]
