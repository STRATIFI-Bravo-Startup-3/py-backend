from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=255)
    api_endpoint = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add any other fields as needed
    
    def __str__(self):
        return self.name


class SocialMediaHandle(models.Model):
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('custom', 'Custom'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE, related_name='handles')
    handle = models.CharField(max_length=255)
    followers = models.PositiveIntegerField(default=0)
    urls = models.ManyToManyField('CustomURL', blank=True)
    custom_url = models.URLField(null=True, blank=True)
    custom_followers = models.IntegerField(default=0)
    last_updated = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'platform')
    
    def __str__(self):
        return f'{self.user.username} - {self.platform.name}: {self.handle}'

class CustomURL(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
