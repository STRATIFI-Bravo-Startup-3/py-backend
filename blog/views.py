
from django.shortcuts import render
from blog.models import BlogPost,Comments,Category
from rest_framework import generics
from . import serializers
from users import permissions
from rest_framework import permissions
from users.permissions import (IsOwnerOrReadOnly,
IsBrandUserOrReadonly,IsInfluencerUserOrReadonly,IsEmployeeUserOrReadonly)
# Create your views here.


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsEmployeeUserOrReadonly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

class BlogPostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsEmployeeUserOrReadonly]
    serializer_class = serializers.BlogPostSerializer
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer
    permission_classes = [IsEmployeeUserOrReadonly]
    
    
    
class CommentList(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsBrandUserOrReadonly]
    
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsBrandUserOrReadonly]
                          
    