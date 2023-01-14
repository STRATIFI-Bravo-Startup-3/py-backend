from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path,include
from .views import (BlogPostList,BlogPostDetail,
CommentDetail,CommentList,CategoryDetail,CategoryList)


urlpatterns = [
    # code omitted for brevity
    re_path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path('posts/', BlogPostList.as_view(), ),
    re_path('posts/<slug:slug>/', BlogPostDetail.as_view()),
    re_path('comments/', CommentList.as_view()),
    re_path('comments/<int:pk>/',CommentDetail.as_view()),
    re_path('categories/',CategoryList.as_view()),
    re_path('categories/<int:pk>/',CategoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)