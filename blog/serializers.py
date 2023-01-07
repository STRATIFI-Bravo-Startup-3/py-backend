from rest_framework import serializers
from . models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'user']
