from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

# router = routers.DefaultRouter()
# router.register(r'characters', views.CharacterViewSet)

urlpatterns = [
	path(r'character/<int:charID>/<str:page>', views.charContent),
	path(r'mcharactercreation/<str:left>/<str:right>/', views.splitPage),
	path(r'mcharactercreation/<str:left>/', views.splitPage),
	path(r'p/<str:pformat>/<str:left>/<str:right>/', views.splitPage),
	path(r'p/<str:pformat>/<str:left>/', views.splitPage),
	path(r'p/<str:pformat>/', views.splitPage),

	# url(r'api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rpgapi')),

]