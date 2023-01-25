from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path,include
# from .views import (BlogPostAPIList,BlogPostAPIDetail,
# CommentDetail,CommentList,CategoryDetail,CategoryList)

from . import views


urlpatterns = [
    # code omitted for brevity
    # re_path('ckeditor/', include('ckeditor_uploader.urls')),
    # re_path('posts/', BlogPostList.as_view(), ),
    # re_path('posts/<slug:slug>/', BlogPostDetail.as_view()),
    # re_path('comments/', CommentList.as_view()),
    # re_path('comments/<int:pk>/',CommentDetail.as_view()),
    # re_path('categories/',CategoryList.as_view()),
    # re_path('categories/<int:pk>/',CategoryDetail.as_view()),
    
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    #re_path('', include('rest.urls', namespace='rest')),
    re_path(r'posts/', views.BlogPostListAPIView.as_view(), name='list'),
    re_path(r'create-posts/', views.BlogPostCreateAPIView.as_view(), name='create'),
    re_path(r'posts/<slugslug>/', views.BlogPostDeleteAPIView.as_view(), name='detail'),
    re_path(r'posts/<slug:slug>/', views.BlogPostUpdateAPIView.as_view(), name='update'),
    re_path(r'posts/<slug:slug>/', views.BlogPostDeleteAPIView.as_view(), name='delete'),


	#CommentAPI
    re_path(r'comments/',views.CommentListAPIView.as_view(), name='list'),
    re_path(r'create-comments', views.CommentCreateAPIView.as_view(), name='create'),
    re_path(r'comments/<slug:slug>', views.CommentDetailAPIView.as_view(), name='thread'),
]

urlpatterns = format_suffix_patterns(urlpatterns)