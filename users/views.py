from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

from .models import (
    BrandProfile,
    InfluencerProfile,
    Campaign,
    Job,
    Influencer,
    InfluencerPool,
)
from .permissions import IsBrandUser, IsInfluencerUser, IsOwnerOrReadOnly
from .serializers import (
    BrandProfileSerializer,
    InfluencerProfileSerializer,
    ProfilePictureSerializer,
    UserCreateSerializer,
    CampaignSerializer,
    JobSerializer,
    BrandProfileSerializer,
    InfluencerProfileSerializer,
    BrandProfileUpdateSerializer,
    InfluencerProfileUpdateSerializer,
    InfluencerPoolSerializer,
    MyUserSerializer,
)

from rest_framework import generics, request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from djoser import signals
from djoser.conf import settings as djoser_settings
from djoser.compat import get_user_email
from djoser.utils import encode_uid
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .emails.email import ActivationEmail, ConfirmationEmail
from rest_framework import serializers
from django.conf import settings

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]

        if settings.DJOSER.get("SEND_ACTIVATION_EMAIL", False):
            ActivationEmail(self.request, context).send(to)
        elif settings.DJOSER.get("SEND_CONFIRMATION_EMAIL", False):
            ConfirmationEmail(self.request, context).send(to)


#########################################


# This is a comment
class BrandOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBrandUser]
    serializer_class = MyUserSerializer

    def get_object(self):
        return self.request.user


class InfluencerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsInfluencerUser]
    serializer_class = MyUserSerializer

    def get_object(self):
        return self.request.user


class BrandListCreateView(generics.ListCreateAPIView):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer


class InfluencerListCreateView(generics.ListCreateAPIView):
    queryset = InfluencerProfile.objects.all()
    serializer_class = InfluencerProfileSerializer


class InfluencerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfluencerProfile.objects.all()
    serializer_class = InfluencerProfileSerializer


# Need this for chat function


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    # other viewset logic

    serializer_class = MyUserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = MyUserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def all(self, request):
        serializer = MyUserSerializer(
            User.objects.all(), many=True, context={"request": request}
        )


################################################3


class BrandProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand_profile = BrandProfile.objects.get(user=request.user)
        serializer = BrandProfileSerializer(brand_profile)
        return Response(serializer.data)


class BrandOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBrandUser]
    serializer_class = MyUserSerializer

    def get_object(self):
        return self.request.user


class InfluencerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        influencer_profile = InfluencerProfile.objects.get(user=request.user)
        serializer = InfluencerProfileSerializer(influencer_profile)
        return Response(serializer.data)


class BrandProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BrandProfileUpdateSerializer

    def get_object(self):
        return BrandProfile.objects.get(user=self.request.user)


# updating user
class InfluencerProfileUpdateView(APIView):
    """
    Description - return response of updated data about the current login user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = InfluencerProfileUpdateSerializer

    def put(self, request: request.Request) -> Response:
        """Updates influencer profile data in full and partial"""

        instance = InfluencerProfile.objects.filter(user=request.user).first()
        serializers = self.serializer_class(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)


class ProfilePictureUpdateView(generics.UpdateAPIView):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePictureSerializer

    def get_object(self):
        return self.request.user


class ProfilePictureView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfilePictureSerializer

    def get_object(self):
        return self.request.user


# data deletion callback
def data_deletion_callback(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id", "")
        try:
            User.objects.filter(id=user_id).first().delete()
            return HttpResponse("Data deletion successful")
        except Exception as e:
            return HttpResponse("Data deletion failed" + str(e))
    else:
        return HttpResponse("Invalid request method")


# CAMPAIGNS
##################################################333
class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            brand_profile = BrandProfile.objects.get(user=self.request.user)
            serializer.save(brand=brand_profile)
        except BrandProfile.DoesNotExist:
            raise ValidationError("Brand Does not exist")


class CampaignUpdateDestroyView(APIView):
    """View to update and delete a campaign making sure only the user created that can do so"""

    permission_classes = [permissions.IsAuthenticated, IsBrandUser]
    serializer_class = CampaignSerializer

    def put(self, request, pk):
        """Updating Campaign created by a user"""
        instance = Campaign.objects.get(brand=request.user, pk=pk)
        serializers = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializers.is_valid(raise_exception=True):
            serializers.save(brand=request.user)
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)

    def delete(self, request, pk):
        """Delete Campaign made by a user"""
        try:
            instance = Campaign.objects.filter(brand=request.user, pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            raise ("The requested data is not found")


class CampaignRetrieveView(generics.RetrieveAPIView):
    """Retrieve a specific campaign"""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    ####################################################################


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        # Only allow creating jobs for campaigns with available influencer pools
        campaign_id = self.request.data["campaign"]
        campaign = Campaign.objects.get(id=campaign_id)
        influencer_pool = InfluencerPool.objects.filter(
            campaign=campaign, status=InfluencerPool.Status.AVAILABLE
        ).first()
        if influencer_pool is None:
            raise serializers.ValidationError(
                "No available influencer for this campaign"
            )
        serializer.save(influencer=influencer_pool.influencer, campaign=campaign)

        # # select the influencer and create a conversation
        # job = serializer.instance
        # conversation = job.campaign.select_influencer(job.influencer)


class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class InfluencerPoolView(generics.ListAPIView):
    serializer_class = InfluencerPoolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        campaign_id = self.kwargs.get("campaign_id")
        campaign = Campaign.objects.get(id=campaign_id)

        if not campaign.is_active:
            raise serializers.ValidationError("This campaign is no longer active")

        if not campaign.is_in_progress:
            raise serializers.ValidationError("This campaign is not yet in progress")

        influencer_pools = InfluencerPool.objects.filter(
            campaign_id=campaign_id, status=InfluencerPool.Status.PENDING
        )
        if not influencer_pools.exists():
            raise serializers.ValidationError(
                "No available influencer for this campaign"
            )

        # If the brand has already selected an influencer, filter out other influencer pools
        if campaign.selected_influencer:
            influencer_pools = influencer_pools.filter(
                influencer=campaign.selected_influencer
            )

        return influencer_pools


class CreateInfluencerPool(APIView):
    serializer_class = InfluencerPoolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        campaign_id = request.data.get("campaign", {})
        influencer = InfluencerProfile.objects.get(user=request.user)

        if InfluencerPool.objects.filter(
            campaign=campaign_id, influencer=influencer
        ).exists():
            raise ValidationError("Influencer already in this pool")
        serializer = self.serializer_class(
            data=request.data, context={"request": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                "status": "Influencer has been added to the pool",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
