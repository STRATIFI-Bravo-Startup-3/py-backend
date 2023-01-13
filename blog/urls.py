from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    # code omitted for brevity
    path('posts/', views.BlogPostList.as_view(), ),
    path('posts/<slug:slug>/', views.BlogPostDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]