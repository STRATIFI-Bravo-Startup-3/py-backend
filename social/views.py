from rest_framework import viewsets
from .serializers import SocialHandlesSerializer
from .models import SocialHandles

class SocialHandelsViewSet(viewsets.ModelViewSet):
    queryset = SocialHandles.objects.all().order_by('?')
    serializer_class = SocialHandlesSerializer