from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SocialHandles

User = get_user_model()

class SocialHandlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialHandles
        fields = '__all__'
