from django.urls import path

from .views import BlogPostList,BlogPostDetail,CommentDetail,CommentList

urlpatterns = [
    path("<slug:slug>",BlogPostList, ),  # new
    path("",BlogPostListDetail, ),
]