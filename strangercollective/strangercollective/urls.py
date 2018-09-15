"""strangercollective URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('polls/', include('polls.urls')),
    # path('jet/', include('jet.urls')), # jet URLS
    path('admin/', admin.site.urls), # admin site
    path(r'markdownx/', include('markdownx.urls')),
    path(r'articles/', include('articles.urls')),
    path(r'tests/', include('tests.urls')),
    path(r'rpg/', include('scrpgtest.urls')),
    path(r'redback/', include('redback.urls')),
    path(r'code/', include('unswcode.urls')),
    path(r'cv/', include('cv.urls')),
    path(r'sc/', include('sc.urls'),name='sc'),
    path(r'', include('home.urls'),name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)