from rest_framework import serializers
from .models import BlogPost,Comments#,Category
from users.models import User

from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer, SerializerMethodField, ValidationError
from users.serializers import UserSerializer
from django.contrib.contenttypes.models import ContentType


#Post Serializers
class BlogPostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'publish'
        ]


post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
        )


class BlogPostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'image',
            'comments',
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        c_qs = Comments.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

class BlogPostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserSerializer(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'user',
            'title',
            'content',
            'created_at'
        ]

#Comment Serializer
def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comments
            fields = [
                'id',
                'content',
                'created',
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comments.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comments.objects.create_by_model_type(
                    model_type, slug, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer



class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comments
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'created',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='comments-api:thread')
    reply_count = SerializerMethodField()
    class Meta:
        model = Comments
        fields = [
            'url',
            'id',
            # 'content_type',
            # 'object_id',
            # 'parent',
            'content',
            'reply_count',
            'created',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentChildSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comments
        fields = [
            'id',
            'user',
            'content',
            'created',
        ]



class CommentDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    replies =   SerializerMethodField()
    class Meta:
        model = Comments
        fields = [
            'id',
            'user',
            #'content_type',
            #'object_id',
            'content',
            'reply_count',
            'replies',
            'created',
            'content_object_url',
        ]
        read_only_fields = [
            #'content_type',
            #'object_id',
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



# class CategorySerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # class Meta:
    #     model = Category
    #     fields = ['id', 'name', 'owner', 'posts']

# class BlogPostSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')

#     class Meta:
#         model = BlogPost
#         fields = ['id', 'title', 'body', 'owner']
        
        
        
# class CommentSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')

#     class Meta:
#         model  = Comments
#         fields = ['id', 'body', 'owner', 'post']



# class UserSerializer(serializers.ModelSerializer):
#     posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'posts', 'comments']