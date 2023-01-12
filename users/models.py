from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django_countries.fields import CountryField
from django_rest_passwordreset.signals import reset_password_token_created

class User(AbstractUser):
    is_influencer=models.BooleanField(default=False)
    is_brand=models.BooleanField(default=False)
    is_employee=models.BooleanField(default=False)


    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    is_verified=models.BooleanField(default=False)

# Have to comment out the profile_pic object before the terminal errors was fix

    #profile_pic = models.ImageField(null=True, blank=True, upload_to="static/profile/images", default="images/user-default.png",)

    def __str__(self) :
        return self.username
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class Influencer(models.Model):
    user=models.OneToOneField(User, related_name="influencer", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    portfolio = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    niche = models.CharField(max_length=200, null=True, blank=True)
    

    def __str__(self):
        return self.user.username



class Brand(models.Model):
    user=models.OneToOneField(User, related_name="employer", on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200, null=True, blank=True)
    niche = models.CharField(max_length=200, null=True, blank=True)
    company_size = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.user.username


class Employee(models.Model):
    user=models.OneToOneField(User, related_name="staff", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)
    staff_id = models.CharField(max_length=200, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.user.username