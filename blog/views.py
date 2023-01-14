
from django.shortcuts import render
from blog.models import BlogPost,Comments
from rest_framework import generics
from . import serializers
from users import permissions
# Create your views here.


class BlogPostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer
    


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        permission_classes = [permissions.IsEmployeeUser]

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer
    permission_classes = [permissions.IsEmployeeUser]
    
    
class CommentList(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsBrandUser]
                          
