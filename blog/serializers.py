from rest_framework import serializers, viewsets
from .models import BlogPost, Comment, Reply  
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework.serializers import (
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from users.serializers import UserSerializer
from django.contrib.contenttypes.models import ContentType


post_detail_url = HyperlinkedRelatedField(
    read_only=True, view_name="blog-posts:detail", lookup_field="slug"
)

class CommentSerializer(ModelSerializer):
    # reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            # "content_type",
            # "object_id",
            # "parent",
            "content",
            # "reply_count",
            "created",
        ]

    # def get_reply_count(self, obj):
    #     if obj.is_parent:
    #         return obj.children().count()
    #     return 0
    
class BlogPostDetailSerializer(ModelSerializer):
    lookup_field = "slug"
    url = post_detail_url
    owner = serializers.ReadOnlyField(source='owner.username')
    image = SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)


    class Meta:
        model = BlogPost
        fields = [
            "id",
            "url",
            "owner",
            "title",
            "slug",
            "content",
            "publish",
            "image",
            "comments",
        ]

    # def get_html(self, obj):
    #     return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class BlogPostListSerializer(ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="blogpost_post_detail", read_only=True
    )
    owner = UserSerializer(read_only=True)
    lookup_field = "slug"

    class Meta:
        model = BlogPost
        fields = [
            "image",
            "url",
            "owner",
            "title",
            "content",
            "created_at",
            "slug",
        ]

class CommentCreateSerializer(CommentSerializer):
    def create(self, validated_data):
        return super().create(validated_data)


class CommentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content")

class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "created",
        ]

class CommentDetailSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            "owner",
            "content",
            "replies",
            "created",
        ]
        read_only_fields = [
            "replies",
        ]

