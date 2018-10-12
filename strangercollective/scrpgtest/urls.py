from django.urls import path
from . import views

app_name = 'scrpgtest'
urlpatterns = [
    path(r'', views.home),
    path(r'card/<int:characterid>/', views.card),
    path(r'character/<int:characterid>/', views.characterdata),
]