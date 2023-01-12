from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class SocialHandles(models.Model):
    user= models.OneToOneField(User, related_name= 'social', on_delete=models.CASCADE)
    website = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    linkedin_followers = models.IntegerField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    facebook_followers = models.IntegerField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    instagram_followers = models.IntegerField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    twitter_followers = models.IntegerField(null=True, blank=True)
    tik_tok_url = models.URLField(null=True, blank=True)
    tit_tok_followers = models.IntegerField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    youtube_subscriber = models.IntegerField(null=True, blank=True)