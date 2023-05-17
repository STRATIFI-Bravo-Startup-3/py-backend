from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer, UserCreateMixin
from .models import (
    BrandProfile,
    InfluencerProfile,
    Campaign,
    Job,
    Influencer,
    InfluencerPool,
)
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import IntegrityError, transaction
from djoser.conf import settings


User = get_user_model()


class MyUserSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ("username", "email", "role")


class UserCreateSerializer(UserCreateSerializer, UserCreateMixin):
    role = serializers.ChoiceField(choices=User.Role.choices)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["username", "id", "email", "password", "role"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"write_only": True},
            "role": {"required": True},
            # "company_name": {"required": [True if fields[3] == "BRAND" else False]},
            # "first_name": {"required": [True if fields[3] == "INFLUENCER" else False]},
            # "last_name": {"required": [True if fields[3] == "INFLUENCER" else False]},
        }

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        try:
            user = self.perform_create(validated_data, role, password)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data, role, password):
        with transaction.atomic():
            user = User.objects.create_user(
                **validated_data, role=role, password=password
            )
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

    # def create(self, validated_data):
    #     role = validated_data.pop("role")
    #     password = validated_data.pop("password")
    #     user = User.objects.create_user(**validated_data, role=role, password=password)
    #     if role == User.Role.BRAND:
    #         company_name = self.initial_data.get("company_name")
    #         brand_profile = BrandProfile(user=user, company_name=company_name)
    #         brand_profile.save()
    #     elif role == User.Role.INFLUENCER:
    #         first_name = self.initial_data.get("first_name")
    #         last_name = self.initial_data.get("last_name")
    #         influencer_profile = InfluencerProfile(
    #             user=user, first_name=first_name, last_name=last_name
    #         )
    #         influencer_profile.save()
    #     return user


class BrandProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = BrandProfile
        fields = "__all__"


class InfluencerProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = BrandProfile
        fields = "__all__"


class BrandProfileUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = BrandProfile
        fields = "__all__"
        read_only_fields = ("user",)


class InfluencerProfileUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = "__all__"
        read_only_fields = ("user",)


class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(write_only=True)

    class Meta:
        model = User
        fields = ("profile_picture",)

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)

        if profile_picture:
            filename = slugify(instance.username)
            path = f"profile_pictures/{filename}"
            if instance.profile_picture.name != "profile_pictures/default.png":
                default_storage.delete(instance.profile_picture.name)
            instance.profile_picture.save(path, ContentFile(profile_picture.read()))

        return super().update(instance, validated_data)


class CampaignSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.BRAND)
    )
    influencer_pool = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            "id",
            "title",
            "description",
            "brand",
            "influencer_type",
            "niches",
            "preferred_platforms",
            "audience_age_brackets",
            "audience_gender",
            "start_date",
            "end_date",
            "budget",
            "influencer_pool",
        ]

    def get_influencer_pool(self, obj):
        influencer_pool = InfluencerPool.objects.filter(
            campaign=obj, status=InfluencerPool.Status.AVAILABLE
        )[:3]
        return InfluencerProfileSerializer(influencer_pool, many=True).data


class InfluencerPoolSerializer(serializers.ModelSerializer):
    influencer = InfluencerProfileSerializer(read_only=True)

    class Meta:
        model = InfluencerPool
        fields = ["id", "influencer", "campaign"]

    def validate(self, data):
        # Check if influencer is already in pool for this campaign
        influencer = data["influencer"]
        campaign = data["campaign"]
        if InfluencerPool.objects.filter(
            influencer=influencer, campaign=campaign
        ).exists():
            raise serializers.ValidationError(
                "Influencer already exists in pool for this campaign"
            )
        return data


class JobSerializer(serializers.ModelSerializer):
    influencer = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    campaign = serializers.PrimaryKeyRelatedField(
        queryset=Campaign.objects.all(), required=True
    )
    brand = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "influencer",
            "campaign",
            "brand",
            "title",
            "description",
            "start_date",
            "end_date",
        ]

    def get_brand(self, obj):
        return obj.campaign.brand.username

    def get_title(self, obj):
        return obj.campaign.title

    def get_description(self, obj):
        return obj.campaign.description

    def get_start_date(self, obj):
        return obj.campaign.start_date

    def get_end_date(self, obj):
        return obj.campaign.end_date
