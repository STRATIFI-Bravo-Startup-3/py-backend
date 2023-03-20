from rest_framework import generics
from .models import SocialHandles
from .serializers import SocialHandlesSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()

class SocialHandlesListCreateView(generics.ListCreateAPIView):
    queryset = SocialHandles.objects.all()
    serializer_class = SocialHandlesSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

class SocialHandlesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialHandles.objects.all()
    serializer_class = SocialHandlesSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
