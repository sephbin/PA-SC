from django.urls import path
from . import views

urlpatterns = [
    path(r'family/<str:familyname>/<str:scripttype>', views.familygetscript),
]