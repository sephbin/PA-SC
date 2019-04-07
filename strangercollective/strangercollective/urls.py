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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from .api import api_router


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
    path(r'api/', include('api.urls'),name='api'),
    path(r'pano/', include('panorama.urls'),name='pano'),
    path(r'', include('home.urls'),name='home'),
    re_path(r'crowbar/', TemplateView.as_view(template_name='index.html')),
    
]

urlpatterns += [
    url(r'^api/v2/', api_router.urls),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^pages/', include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)