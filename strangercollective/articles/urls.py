from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path(r'create/', views.post_create),
    path(r'detail/<int:article_id>/', views.post_detail, name='post_detail'),
    path(r'list/', views.post_list),
    path(r'detail/<int:article_id>/edit', views.post_update),
    path(r'delete/', views.post_delete),
]