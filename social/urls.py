from django.urls import re_path, path, include
from .views import SocialHandelsViewSet
from rest_framework import routers

router = routers.DefaultRouters()

router.register(r'socials', SocialHandelsViewSet)

urlpatterns=[
    re_path('', include(router.urls)),
    re_path('', include('rest_framework.urls', namespace='rest_framework'))

]

