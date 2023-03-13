"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import re_path, include
from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token
#from social_django.urls import patterns as social_django_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    re_path('admin/', admin.site.urls),
#    re_path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
#    re_path(
#        'api/docs/',
#        SpectacularSwaggerView.as_view(url_name='api-schema'),
#        name='api-docs'),
    re_path('api-auth/', include('rest_framework.urls')),
    re_path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    re_path('', include("users.urls")),
    re_path('', include("about.urls")),
    re_path('blog/', include("blog.urls")),
   # re_path('social-auth/', include('social_django.urls', namespace='social')),
]

