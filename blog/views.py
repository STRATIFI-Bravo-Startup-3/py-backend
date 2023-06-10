from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.shortcuts import render, get_object_or_404
from blog.models import BlogPost, Comment #,Category
from rest_framework import generics
from . import serializers
from .serializers import create_comment_serializer
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
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
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
# class CommentCreateAPIView(CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = serializers.CommentCreateSerializer
    
    
    
    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     #content_type =request.META['CONTENT_TYPE']
    #     # object_id = data.get('object_id')
        
    #     comment = Comment.objects.create(
    #         content=data['content'],
    #         # content_type=content_type,
    #         # object_id=object_id,
    #     )

    #     return Response(comment.data, status=201)



    # def get_serializer_class(self):
    #     model_type = self.request.GET.get("type")
    #     slug = self.request.GET.get("slug")
    #     parent_id = self.request.GET.get("parent_id", None)
    #     return create_comment_serializer(
    #             model_type=model_type, 
    #             slug=slug, 
    #             parent_id=parent_id,
    #             user=self.request.user
    #             )

    #permission_classes = [IsAuthenticated]

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


class CommentDetailAPIView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        return obj


class CommentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        slug = self.request.GET.get("slug")
        model_type = self.request.GET.get("type")
        if slug and model_type:
            try:
                content_type = ContentType.objects.get(model=model_type)
                obj = content_type.get_object_for_this_type(slug=slug)
            except:
                return Comment.objects.none()
            queryset = obj.comments.all().order_by("-timestamp")
            query = self.request.GET.get("q")
            if query:
                queryset = queryset.filter(
                        Q(content__icontains=query)|
                        Q(user__first_name__icontains=query) |
                        Q(user__last_name__icontains=query)
                        ).distinct()
            return queryset
        return Comment.objects.none()

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(BlogPost, id=post_id)
        serializer.save(author=self.request.user, post=post)
    
class CommentEditAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentEditSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentChildListAPIView(generics.ListAPIView):
    # serializer_class = serializers.CommentListCreateSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        parent_id = self.kwargs.get("parent_id")
        if parent_id:
            queryset = Comment.objects.filter(parent=parent_id).order_by("-timestamp")
            query = self.request.GET.get("q")
            if query:
                queryset = queryset.filter(
                        Q(content__icontains=query)|
                        Q(user__first_name__icontains=query) |
                        Q(user__last_name__icontains=query)
                        ).distinct()
            return queryset
        return Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

                          
