from django.urls import path
from . import views

app_name = 'redback'
urlpatterns = [
    # path(r'<int:id>/', views.index),
    path(r'example/', views.three),
]