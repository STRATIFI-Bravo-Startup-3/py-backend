from django.contrib import admin
from django.urls import path
from .views import Home, about, PageView, vission, mission, goal, service

from . import views
#app_name = "about"

urlpatterns = [
    path('', Home, name='home'),
    path('about', views.about, name='about'),
    path('vission', views.vission, name='vission'),
    path('mission', views.mission, name='mission'),
    path('goal', views.goal, name='goal'),
    path('service', views.service, name='service'),
    #path('', PageView.as_view()),
    path('<slug:slug>', PageView.as_view(), name="page_detail"),
]

