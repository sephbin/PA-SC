from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views

urlpatterns = [
	path(r'', views.solve),

	path(r'packMono/', views.packMono),
	path(r'packGeom/', views.packGeom),
	path(r'objectCRUD/', views.objectCRUD),
]

# solvepatterns = []
# for u in urlpatterns:
# 	pattern = eval(u.pattern.describe())
# 	solvepatterns.append(path(pattern+r"solve", u.callback))
# 	solvepatterns.append(path(pattern+r"solve/", u.callback))

# urlpatterns = urlpatterns+solvepatterns