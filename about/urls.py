from django.contrib import admin
from django.urls import path
from .views import Home, Aboutus, PageView

#app_name = "about"

urlpatterns = [
    path('', Home, name='home'),
    path('about-us', Aboutus, name='aboutus'),
    #path('', PageView.as_view()),
    path('<slug:slug>', PageView.as_view(), name="page_detail"),
]

