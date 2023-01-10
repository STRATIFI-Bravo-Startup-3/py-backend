from rest_framework import serializers
from .models import SocialHandles


class SocialHandlesSerializer(serializers.ModelSerializer):
    class Meta:
        model=SocialHandles
        fields='__all__'