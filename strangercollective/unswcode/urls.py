from django.urls import path
from . import views

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
    path(r'get_test_question/<str:question>', views.get_test_question),
]
