from django.urls import path
from . import views

app_name = 'unswcode'
urlpatterns = [
    path(r'', views.codeHome),
    path(r'lecture/<int:lecture_wk>', views.lecture),
    path(r'submit/<str:ass_no>', views.submit),
    path(r'marking', views.marking),
    path(r'submitPost/', views.submitPost),
]