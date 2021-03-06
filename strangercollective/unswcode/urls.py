from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'buildingcomponents', views.buildingComponentViewSet)



app_name = 'unswcode'
urlpatterns = [
    path(r'', views.codeHome),
    path(r'lecture/<int:lecture_wk>', views.lecture),
    path(r'submit/<str:ass_no>', views.submit),
    path(r'view/<int:ass_id>', views.viewmark),
    path(r'marking/<str:ass_no>', views.marking),
    path(r'submitPost/', views.submitPost),
    path(r'start_test/<str:testid>/<str:idi>/<str:password>/', views.start_test),
    path(r'submit_test_question/', views.submit_test_question),
    path(r'test/results/<str:testName>', views.marklist),
    path(r'get_test_question/<str:question>', views.get_test_question),
    path(r'function/changemarks', views.changemarks),
    url(r'^api/', include(router.urls)),
    path(r'api/uploadBuildingComponent/', views.uploadBuildingComponent),
    url(r'^api/api-auth/', include('rest_framework.urls')),
]
