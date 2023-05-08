# serializers.py
from rest_framework import serializers
from .models import SocialMediaHandle, SocialMediaPlatform, CustomURL
from django.contrib.auth import get_user_model
from .models import SocialMediaHandle, SocialMediaPlatform


User = get_user_model()

class SocialHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = ['platform', 'handle', 'follower_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CustomURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomURL
        fields = ['id', 'url']
        read_only_fields = ['id']

class CustomSocialHandleSerializer(serializers.ModelSerializer):
    urls = CustomURLSerializer(many=True, read_only=True)

    class Meta:
        model = SocialMediaHandle
        fields = ['id', 'platform', 'handle', 'followers', 'urls', 'custom_url', 'custom_followers', 'last_updated']
        read_only_fields = ['id', 'last_updated']

    def validate(self, data):
        # Add any validation logic for the serializer fields here
        return data

    def create(self, validated_data):
        # Create a new SocialMediaHandle instance
        social_handle = SocialMediaHandle(**validated_data)
        social_handle.user = self.context['request'].user  # Set the user from request context
        social_handle.save()
        return social_handle

    def update(self, instance, validated_data):
        # Update an existing SocialMediaHandle instance
        instance.handle = validated_data.get('handle', instance.handle)
        instance.followers = validated_data.get('followers', instance.followers)
        instance.custom_url = validated_data.get('custom_url', instance.custom_url)
        instance.custom_followers = validated_data.get('custom_followers', instance.custom_followers)
        instance.last_updated = validated_data.get('last_updated', instance.last_updated)
        instance.save()
        return instance
        
class SocialMediaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPlatform
        fields = ['id', 'name', 'api_endpoint']
        read_only_fields = ['id']


class FacebookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = '__all__'

class FacebookFollowerSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField()

    class Meta:
        model = SocialMediaHandle
        fields = ['id', 'platform', 'username', 'follower_count', 'user']
        read_only_fields = ['id', 'user']


class TwitterHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = '__all__'

class TwitterFollowerCountSerializer(serializers.Serializer):
    follower_count = serializers.IntegerField()


class InstagramHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = ['id', 'platform', 'username', 'followers', 'user']
        read_only_fields = ['id', 'followers', 'user']


class InstagramConnectionSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    

class YouTubeHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = ('id', 'platform', 'username', 'followers')

class YouTubeConnectSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class TikTokHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = ('id', 'platform', 'handle', 'follower', 'tiktok_username', 'tiktok_password')
        read_only_fields = ('id', 'platform', 'handle', 'follower')


class TikTokConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaHandle
        fields = ('id', 'platform', 'username', 'followers')
        read_only_fields = ('id', 'platform', 'username', 'followers')

    def create(self, validated_data):
        # Create a new SocialMediaHandle instance for TikTok connection
        social_handle = SocialMediaHandle(**validated_data)
        social_handle.platform = SocialMediaPlatform.TIKTOK  # Set platform as TikTok
        social_handle.user = self.context['request'].user  # Set the user from request context
        social_handle.save()
        return social_handle

    def update(self, instance, validated_data):
        # Update an existing SocialMediaHandle instance for TikTok connection
        instance.username = validated_data.get('username', instance.username)
        instance.followers = validated_data.get('followers', instance.followers)
        instance.save()
        return instance
