from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register(r'characters', views.CharacterViewSet)
router.register(r'races', views.RaceViewSet)
router.register(r'possessions', views.PossessionViewSet)
router.register(r'campaigns', views.CampaignViewSet)

app_name = 'scrpgtest'
urlpatterns = [
	path(r'character/<int:characterid>', views.charPage),
	path(r'card/<int:characterid>/<str:cardid>', views.csCard),
	path(r'api/editattr/<int:characterid>/<str:attrid>/<str:attrval>', views.editattr),
	path(r'api/newpos/<int:characterid>/<int:possessionid>', views.newpos),
	path(r'api/rempos/<int:characterid>/<int:possessionid>', views.rempos),
	path(r'api/editskill/<int:characterid>/<int:skillid>/<int:rank>', views.editskill),
	path(r'api/remskill/<int:characterid>/<int:skillid>', views.remskill),
	path(r'api/newskill/<int:characterid>/<int:skillid>', views.newskill),
	path(r'api/newadvantage/<int:characterid>/<int:traitid>', views.newadvantage),
	path(r'api/remadvantage/<int:characterid>/<int:traitid>', views.remadvantage),
	path(r'api/ediadvantagemodal/<int:characterid>/<int:traitid>', views.ediadvantagemodal),
	url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rpgapi')),
    # path(r'', views.home),
    # path(r'card/<int:characterid>/', views.card),
    # path(r'character/<int:characterid>/', views.characterdata),
    # path(r'characterlist/', views.characterlist),
]