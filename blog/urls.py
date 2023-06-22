from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path,include,path
from .views import (BlogPostListAPIView,
    BlogPostDetailAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    CommentEditAPIView,
    CommentDeleteAPIView,
    )

app_name = 'blog'

# from rest_framework.routers import SimpleRouter
# router = SimpleRouter()
# router.register("posts", PostViewSet)


urlpatterns = [
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('posts/', BlogPostListAPIView.as_view(), name='post_list'),
    #path('posts/create', BlogPostCreateAPIView.as_view(), name='post_create'),
    path('posts/<slug:slug>/', BlogPostDetailAPIView.as_view(), name='post_detail'),
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('comments/list/', CommentListAPIView.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    path('comments/<int:post_id>/list-create/', CommentCreateAPIView.as_view(), name='comment_list_create'),
    path('comments/<int:pk>/edit/', CommentEditAPIView.as_view(), name='comment_edit'),
    path('comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment_delete'),
]




# urlpatterns = format_suffix_patterns(urlpatterns)