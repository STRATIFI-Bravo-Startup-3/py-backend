from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_countries.fields import CountryField

# from chats.models import Message, Conversation


# from social.models import SocialMediaHandles
# from chats.models import Conversation, Message

# some updates

import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class RenameProfilePicture:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{instance.username}.{ext}"
        return os.path.join(self.path, filename)


class User(AbstractUser):
    class Role(models.TextChoices):
        OTHER = "OTHER", "Other"
        ADMIN = "ADMIN", "Admin"
        BRAND = "BRAND", "Brand"
        INFLUENCER = "INFLUENCER", "Influencer"

    role = models.CharField(max_length=50, choices=Role.choices)
    profile_picture = models.ImageField(
        upload_to=RenameProfilePicture("profile_pictures/"),
        default="profile_pictures/default.png",
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

            if self.role == self.Role.BRAND:
                BrandProfile.objects.create(user=self)
            elif self.role == self.Role.INFLUENCER:
                InfluencerProfile.objects.create(user=self)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.role


class Niche(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AgeBracket(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CompanySize(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class InfluencerType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BrandManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.BRAND)


class Brand(User):
    base_role = User.Role.BRAND
    brand = BrandManager()

    REQUIRED_FIELDS = ["company_name", "contact_person"]

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for brands"


class BrandProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="brand_profile", unique=True
    )
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    ratings = models.PositiveIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    

    class CompanySize(models.TextChoices):
        MICRO = "Micro", "1-9 employees"
        SMALL = "Small", "10-49 employees"
        MEDIUM = "Medium", "50-249 employees"
        LARGE = "Large", "250-999 employees"
        ENTERPRISE = "Enterprise", "1000+ employees"

    company_size = models.CharField(
        max_length=20, choices=CompanySize.choices, default=CompanySize.MICRO
    )
    languages = models.ManyToManyField(Language, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    niches = models.ManyToManyField(Niche, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    budget = models.IntegerField(blank=True, null=True)
    influencer_type = models.ManyToManyField(InfluencerType, blank=True)
    audience_gender = models.ManyToManyField(Gender, blank=True)
    audience_age_brackets = models.ManyToManyField(AgeBracket, blank=True)
    preferred_platform = models.CharField(
        Platform, max_length=200, null=True, blank=True
    )
    secondary_platforms = models.ManyToManyField(
        Platform, related_name="brand", blank=True
    )
    expected_income = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.company_name)


class InfluencerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.INFLUENCER)


class Influencer(User):
    base_role = User.Role.INFLUENCER
    influencer = InfluencerManager()

    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for influencers"


class InfluencerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="influencer_profile", unique=True
    )
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    ratings = models.PositiveIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    languages = models.ManyToManyField(Language, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("CNTS", "Choose Not To Say"),
    )
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True, null=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    primary_niche = models.CharField(Niche, max_length=200, null=True, blank=True)
    other_niches = models.ManyToManyField(Niche, related_name="influencers", blank=True)
    portfolio = models.TextField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    audience_gender = models.ManyToManyField(
        Gender, related_name="influencers", blank=True
    )
    audience_age_brackets = models.ManyToManyField(
        AgeBracket, related_name="influencers", blank=True
    )
    main_platform = models.CharField(Platform, max_length=200, null=True, blank=True)
    secondary_platforms = models.ManyToManyField(
        Platform, related_name="influencers", blank=True
    )
    expected_income = models.IntegerField(blank=True, null=True)
    # social_handles = models.OneToOneField(SocialMediaHandles, on_delete=models.CASCADE, related_name='influencer')

    def __str__(self) -> str:
        return str(self.first_name)


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # update foreign key from user to  brandprofile
    brand = models.ForeignKey(
        BrandProfile, on_delete=models.CASCADE, related_name="campaigns"
    )
    influencer_type = models.ManyToManyField(InfluencerType, blank=True)
    niches = models.ManyToManyField(Niche, blank=True)
    preferred_platforms = models.ManyToManyField(
        Platform, related_name="preferred_platform", blank=True
    )
    audience_age_brackets = models.ManyToManyField(AgeBracket, blank=True)
    audience_gender = models.ManyToManyField(Gender, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    # def select_influencer(self, influencer):
    #     # create a conversation and add brand and influencer to it
    #     conversation = Conversation.objects.create(name=f"{self.title} Conversation")
    #     conversation.online.add(self.brand)
    #     conversation.online.add(influencer)

    #     # create a message from brand to influencer
    #     message = Message.objects.create(
    #         conversation=conversation,
    #         from_user=self.brand,
    #         to_user=influencer,
    #         content=f"You have been selected for the {self.title} campaign.",
    #     )

    # # return the conversation object
    # return conversation


class InfluencerPool(models.Model):
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    selected_by = models.ForeignKey(
        InfluencerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="selected_influencer_pools",
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="influencer_pool"
    )
    influencer_profile = models.ForeignKey(
        Influencer, on_delete=models.CASCADE, related_name="influencer_pool", null=True
    )

    class Status(models.TextChoices):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"
        AVAILABLE = "AVAILABLE"

    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING
    )


class Job(models.Model):
    influencer = models.ForeignKey(
        InfluencerProfile, on_delete=models.CASCADE, related_name="jobs"
    )
    influencer_pool = models.OneToOneField(
        InfluencerPool, on_delete=models.CASCADE, default=None
    )
    start_date = models.DateField()
    end_date = models.DateField()
    compensation = models.DecimalField(max_digits=10, decimal_places=2)
