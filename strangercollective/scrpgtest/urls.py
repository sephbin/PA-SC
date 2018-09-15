from django.urls import path
from . import views

app_name = 'scrpgtest'
urlpatterns = [
    path(r'', views.home),
    path(r'advantagecard/<int:characterid>', views.advantagecard),
]