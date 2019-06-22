from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path(r'', views.home),
    path(r'temp', views.temp),
    path(r'getpage/<str:pageParent>/<str:pageSlug>', views.getPage),
    path(r'map', views.map),
]