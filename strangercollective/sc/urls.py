from django.urls import path
from . import views


app_name = 'sc'
urlpatterns = [
    path('signup/', views.signup_view, name='sc_signup'),
    path('login/', views.login_view, name='sc_login'),
    path('logout/', views.logout_view, name='sc_logout'),
]