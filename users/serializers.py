from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import BrandProfile, InfluencerProfile, Campaign, Job
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify



User = get_user_model()

class MyUserSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices)
    
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('username', 'email', 'role')


class UserCreateSerializer(UserCreateSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'write_only': True},
            'role': {'required': True},
            'company_name': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
            
        }
        
    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, role=role, password=password)
        if role == User.Role.BRAND:
            company_name = self.initial_data.get('company_name')
            brand_profile = BrandProfile(user=user, company_name=company_name)
            brand_profile.save()
        elif role == User.Role.INFLUENCER:
            first_name = self.initial_data.get('first_name')
            last_name = self.initial_data.get('last_name')
            influencer_profile = InfluencerProfile(user=user, first_name=first_name, last_name=last_name)
            influencer_profile.save()
        return user




class BrandProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = BrandProfile
        fields = ('__all__')
        

class InfluencerProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = BrandProfile
        fields = ('__all__')


class BrandProfileUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = BrandProfile
        fields = '__all__'
        read_only_fields = ('user',)

class InfluencerProfileUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = '__all__'
        read_only_fields = ('user',)

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(write_only=True)

    class Meta:
        model = User
        fields = ('profile_picture',)

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)

        if profile_picture:
            filename = slugify(instance.username)
            path = f"profile_pictures/{filename}"
            if instance.profile_picture.name != 'profile_pictures/default.png':
                default_storage.delete(instance.profile_picture.name)
            instance.profile_picture.save(path, ContentFile(profile_picture.read()))

        return super().update(instance, validated_data)

class CampaignSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source='brand.username')

    class Meta:
        model = Campaign
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    influencer = serializers.ReadOnlyField(source='influencer.username')

    class Meta:
        model = Job
        fields = '__all__'