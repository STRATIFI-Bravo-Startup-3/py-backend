from rest_framework import viewsets
from .serializers import SocialHandlesSerializer
from .models import SocialHandles
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated 


User = get_user_model()

class SocialHandelsViewSet(viewsets.ModelViewSet):
    queryset = SocialHandles.objects.all().order_by('?')
    serializer_class = SocialHandlesSerializer

class SocialHandleCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SocialHandlesSerializer
    permission_classes=[permissions.IsAuthenticated]

class SocialHandelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = SocialHandlesSerializer

class SociaLHandleUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = SocialHandlesSerializer