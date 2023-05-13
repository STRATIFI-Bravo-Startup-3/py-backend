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

    role = models.CharField(max_length=50, choices=Role.choices)
    profile_picture = models.ImageField(upload_to=RenameProfilePicture('profile_pictures/'), default='profile_pictures/default.png')

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.role:
                self.role = self.Role.OTHER
        return super().save(*args, **kwargs)


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
    if created and instance.role == User.Role.BRAND:
        BrandProfile.objects.create(user=instance)


class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brand_profile')
    brand_id = models.IntegerField(null=True, blank=True)
    company_name=models.CharField(max_length=200, null=True, blank=True)

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
    languages = models.ManyToManyField(Language, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)


@receiver(post_save, sender=Influencer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.INFLUENCER:
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