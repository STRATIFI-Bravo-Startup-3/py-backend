from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ckeditor_uploader import views as ckeditor_views


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    #path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    
    path('accounts/', include('allauth.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor_upload/', ckeditor_views.upload, name='ckeditor_upload'),

    
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
    
]

#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))] 
