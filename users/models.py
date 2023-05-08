from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
#from social.models import SocialMediaHandles

import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

@deconstructible
class RenameProfilePicture:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{instance.username}.{ext}"
        return os.path.join(self.path, filename)


class User(AbstractUser):
    class Role(models.TextChoices):
        OTHER = "OTHER", "Other"
        ADMIN = "ADMIN", "Admin"
        BRAND = "BRAND", "Brand"
        INFLUENCER = "INFLUENCER", "Influencer"

    base_role = Role.INFLUENCER

    role = models.CharField(max_length=50, choices=Role.choices)
    
    profile_picture = models.ImageField(upload_to=RenameProfilePicture('profile_pictures/'), default='profile_pictures/default.png')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


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

    class Meta:
        proxy = True
    

    def welcome(self):
        return "Only for brands"


@receiver(post_save, sender=Brand)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "BRAND":
        BrandProfile.objects.create(user=instance)


class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brand_profile')
    brand_id = models.IntegerField(null=True, blank=True)
    RATING_CHOICES =(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    ratings = models.PositiveIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    company_name=models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    company_size = models.CharField(max_length=200, null=True, blank=True)
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
    preferred_platform = models.CharField(Platform, max_length=200, null=True, blank=True)
    secondary_platforms = models.ManyToManyField(Platform, related_name='brand', blank=True)
    expected_income = models.IntegerField(blank=True, null=True)


class InfluencerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.INFLUENCER)


class Influencer(User):
    base_role = User.Role.INFLUENCER
    influencer = InfluencerManager()

    class Meta:
        proxy = True
    

    def welcome(self):
        return "Only for influencers"


class InfluencerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="influencer_profile")
    influencer_id = models.IntegerField(null=True, blank=True)
    RATING_CHOICES =(
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
        ('M', 'Male'),
        ('F', 'Female'),
        ('CNTS', 'Choose Not To Say'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    primary_niche = models.CharField(Niche, max_length=200, null=True, blank=True)
    other_niches = models.ManyToManyField(Niche, related_name='influencers', blank=True)
    portfolio = models.TextField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    audience_gender = models.ManyToManyField(Gender, related_name='influencers', blank=True)
    audience_age_brackets = models.ManyToManyField(AgeBracket, related_name='influencers', blank=True)
    main_platform = models.CharField(Platform, max_length=200, null=True, blank=True)
    secondary_platforms = models.ManyToManyField(Platform, related_name='influencers', blank=True)
    expected_income = models.IntegerField(blank=True, null=True)
    #social_handles = models.OneToOneField(SocialMediaHandles, on_delete=models.CASCADE, related_name='influencer')



@receiver(post_save, sender=Influencer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "INFLUENCER":
        InfluencerProfile.objects.create(user=instance)


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    influencer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    start_date = models.DateField()
    end_date = models.DateField()
    compensation = models.DecimalField(max_digits=10, decimal_places=2)