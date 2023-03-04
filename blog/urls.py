from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path,include,path
from blog.serializers import PostViewSet
from blog.views import PostDetail,PostList

# from rest_framework.routers import SimpleRouter
# router = SimpleRouter()
# router.register("posts", PostViewSet)

from . import views


urlpatterns = [
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    #re_path('', include('rest.urls', namespace='rest')),
    # path("", include(router.urls)),
    re_path(r'posts/', views.PostList.as_view(), name='list'),
    re_path(r'post/<slug:slug>/', views.PostDetail.as_view(), name='detail'),
    # re_path(r'posts/<slug:slug>/', views.BlogPostDeleteAPIView.as_view(), name='detail'),
    # re_path(r'posts/<slug:slug>/', views.BlogPostUpdateAPIView.as_view(), name='update'),
    # re_path(r'posts/<slug:slug>/', views.BlogPostDeleteAPIView.as_view(), name='delete'),


	#CommentAPI
    # re_path(r'comments/',views.CommentListAPIView.as_view(), name='list'),
    # re_path(r'create-comments', views.CommentCreateAPIView.as_view(), name='create'),
    # re_path(r'comments/<slug:slug>', views.CommentDetailAPIView.as_view(), name='thread'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)