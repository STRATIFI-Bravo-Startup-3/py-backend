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

    def __str__(self) :
        return self.username
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

RATING_CHOICES =(
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

NICHE_CHOICES =(
    ('Entertainment', 'Entertainment'),
    ('Hospitalities', 'Hospitalities'),
    ('Football', 'Football'),
)


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('CNTS', 'Choose Not To Say'),
    )

LANGUAGES = (
    ('English', 'English'),
    ('Portuguese', 'Portuguese'),
    ('Spanish', 'Spanish'),
    ('Hindi', 'Hindi'),
    ('Russian', 'Russian'),
    ('Japanese', 'Japanese'),
    ('Arabic', 'Arabic'),
    ('French', 'French'),
    ('Italian', 'Italian'),
    ('Turkish', 'Turkish'),
    ('Hausa', 'Hausa'),
    ('Igbo', 'Igbo'),
    ('Yoruba', 'Yoruba'),
)

class Language(models.Model):
    language = models.CharField(max_length=200, unique=True, choices=LANGUAGES, null=True, blank=True)
 
    def __str__(self):
        return self.language
        

class Niche(models.Model):
     niche = models.CharField(max_length=200, unique=True, choices=NICHE_CHOICES, null=True, blank=True)

     def __str__(self):
        return self.niche


  
class Influencer(models.Model):
    user=models.OneToOneField(User, related_name="influencer", on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    ratings = models.PositiveIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    languages = models.ManyToManyField(Language, max_length=20,blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    niches = models.ManyToManyField(Niche, max_length=200, blank=True)
    portfolio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    
    def __str__(self):
        return self.user.username
    
    
class Brand(models.Model):
    user=models.OneToOneField(User, related_name="employer", on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    company_name=models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    company_size = models.CharField(max_length=200, null=True, blank=True)
    languages = models.ManyToManyField(Language, max_length=20,blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    niches = models.ManyToManyField(Niche, max_length=200, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics',null=True, blank=True)
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
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    country = CountryField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.user.username


           