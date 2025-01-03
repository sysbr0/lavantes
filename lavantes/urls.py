"""
URL configuration for accounting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path , include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from  main.views import *




from django.contrib.sitemaps.views import sitemap

from biles.sitemap import *

sitemaps = {
   'products': MainProductSitemap,
}




urlpatterns = [
   path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path("admin/", admin.site.urls),
       path("main/", include('main.urls')), 
       path("account/" , include('users.urls')),
       path("biles/" , include('biles.urls')),
       path("customers/" , include('customers.urls')),
       path('employe/', include('employe.urls')),
       path('api/', include('api.urls')),
       path('payment/', include('money.urls')),

        path('', include('home.urls')),
        path('clints/', include('clints.urls')),
           path('chat/', include('chat.urls')),




]


 
 

# Serve static files during development
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)