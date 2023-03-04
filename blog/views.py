
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from blog.models import BlogPost,Comments#,Category
from rest_framework import generics
from . import serializers
from .serializers import create_comment_serializer
from users import permissions
from .forms import BlogPostForm
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .pagination import PostPageNumberPagination
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from users.permissions import (IsOwnerOrReadOnly, AuthorModifyOrReadOnly,IsAdminUserForObject)

from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models import Q
# Create your views here.


# class CategoryList(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#     # permission_classes = [IsEmployeeUserOrReadonly]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#     permission_classes = [IsOwnerOrReadOnly]
    
    
          
class PostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostListSerializer
    permission_classes = [AllowAny]
    search_fields = ['title', 'content', 'slug']
    lookup_field = 'slug'
    
    
    def get_queryset(self, *args, **kwargs):
        queryset_list = BlogPost.objects.all() #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
    


class PostDetail(generics.RetrieveAPIView):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostDetailSerializer
    pagination_class = PostPageNumberPagination 
    
    

    
    
#Comment API
class CommentCreateAPIView(CreateAPIView):
    queryset = Comments.objects.all()
    #serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type, 
                slug=slug, 
                parent_id=parent_id,
                user=self.request.user
                )


class CommentListAPIView(ListAPIView):
    serializer_class = serializers.CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Comments.objects.filter(id__gte=0) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list

        

# class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
#     queryset = Comments.objects.filter(id__gte=0)
#     serializer_class = serializers.CommentDetailSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
                          
