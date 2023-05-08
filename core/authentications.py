from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from social_core.backends.google import GoogleOAuth2Backend
from users.models import Influencer, Brand

User = get_user_model()

class CustomGoogleOAuth2Backend(GoogleOAuth2Backend):
    def get_user_details(self, response):
        email = response['email']

        return {
            'username': email,
            'email': email,
        }

    def user_data(self, access_token, *args, **kwargs):
        data = super().user_data(access_token, *args, **kwargs)
        data['email'] = data.get('email', '').lower()
        return data

    def create_user(self, *args, **kwargs):
        user = super().create_user(*args, **kwargs)
        role = kwargs.get('role')
        if user.role == User.Role.BRAND:
            Brand.objects.create(user=user)
        elif user.role == User.Role.INFLUENCER:
            Influencer.objects.create(user=user)
        return user

# Handle lowercase email addresses
@receiver(pre_save, sender=User)
def lowercase_email(sender, instance, *args, **kwargs):
    instance.email = instance.email.lower()
