from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

# router = routers.DefaultRouter()
# router.register(r'characters', views.CharacterViewSet)

urlpatterns = [
	path(r'mcharactercreation/<str:left>/<str:right>/', views.splitPage),
	path(r'mcharactercreation/<str:left>/', views.splitPage),

	# url(r'api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rpgapi')),

]