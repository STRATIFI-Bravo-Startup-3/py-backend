from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.shortcuts import render, get_object_or_404
from blog.models import BlogPost, Comment #,Category
from rest_framework import generics
from . import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .pagination import PostPageNumberPagination
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from users.permissions import (IsOwnerOrReadOnly, AuthorModifyOrReadOnly,IsAdminUserForObject)
from django.contrib.contenttypes.models import ContentType

from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models import Q

 #POSTS API         
class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostListSerializer
    permission_classes = [AllowAny,]
    search_fields = ['title', 'content', 'slug']
    
    def get_queryset(self, *args, **kwargs):
        queryset_list = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
    


class BlogPostDetailAPIView(generics.RetrieveAPIView):
    #permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostDetailSerializer
    lookup_field = 'slug'

    pagination_class = PostPageNumberPagination
    
    def get_queryset(self, *args, **kwargs):
        queryset_list = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list 
    

    
    
#Comment API
class CommentListAPIView(ListAPIView):
    serializer_class = serializers.CommentListSerializer
    permission_classes = [AllowAny, IsAuthenticatedOrReadOnly]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination 

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
    
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        # post_id = self.kwargs['post_id']
        post = get_object_or_404(BlogPost)
        serializer.save(owner=self.request.user, post=posst) 

class CommentDetailAPIView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        return obj 
    
class CommentEditAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentEditSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]




                          
