from django.urls import path
from . import views

app_name = 'tests'
urlpatterns = [
    path(r'ortho', views.ortho),
    path(r'tokenpos/<str:id>/<str:x>/<str:y>/<str:z>/', views.tokenpos),
    path(r'updated/<str:id>/<str:date>/', views.ismapupdated),
    path(r'table/', views.table),
    path(r'dir', views.dir),
]