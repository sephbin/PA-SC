from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    path(r'map/<str:whatmap>', views.mapview),
]