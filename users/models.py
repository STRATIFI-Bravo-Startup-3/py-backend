from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django_countries.fields import CountryField

class User(AbstractUser):
    is_influencer=models.BooleanField(default=False)
    is_brand=models.BooleanField(default=False)
    is_employee=models.BooleanField(default=False)


    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    is_verified=models.BooleanField(default=False)

# Have to comment out the profile_pic object before the terminal errors was fix

    #profile_pic = models.ImageField(null=True, blank=True, upload_to="static/profile/images", default="images/user-default.png",)

    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self) :
        return self.username
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('CNTS', 'Choose Not To Say'),
    )


NICHES = (
    ('Sc', 'Science'),
    ('Sp', 'Sport'),
    ('Et', 'Entertainment'),
    ('Tc', 'Tech'),
    ('Ht', 'Health'),
    ('Bs', 'Business'),
    ('Ot', 'Others'),
    )

LANGUAGES = (
    ('en', 'English'),
    ('pt', 'Portuguese'),
    ('sp', 'Spanish'),
    ('Hi', 'Hindi'),
    ('Ru', 'Russian'),
    ('Ja', 'Japanese'),
    ('Ar', 'Arabic'),
    ('Fr', 'French'),
    ('It', 'Italian'),
    ('Tu', 'Turkish'),
    ('Hu', 'Hausa'),
    ('ig', 'Igbo'),
    ('Yo', 'Yoruba'),
    ('Pg', 'Pidgin'),
    ('Ur', 'Urhobo'),
)
    

class Influencer(models.Model):
    user=models.OneToOneField(User, related_name="influencer", on_delete=models.CASCADE)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, blank=True, null=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    niche = models.CharField(max_length=200, choices=NICHES, verbose_name="Please select your niche", null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, blank=True, verbose_name="Please select your languages", null=True)
    portfolio = models.TextField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    
    

    def __str__(self):
        return self.user.username



class Brand(models.Model):
    user=models.OneToOneField(User, related_name="employer", on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    company_size = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    niche = models.CharField(max_length=200, choices=NICHES, verbose_name="Please select your niche", null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, verbose_name="Please select your languages", blank=True, null=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    budget = models.IntegerField(blank=True, null=True)


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