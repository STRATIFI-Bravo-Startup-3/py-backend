from django.http import request, HttpResponseRedirect, Http404
from rest_framework import generics, authentication, permissions, status, generics
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import (InfluencerSignupSerializer, PasswordResetSerializer, 
EmployeeSignupSerializer, BrandSignupSerializer, InfluencerProfileSerializer,
BrandProfileSerializer, EmployeeProfileSerializer, ProfilePictureUpdateSerializer,
UserSerializer, ChangePasswordSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsBrandUser, IsInfluencerUser, IsEmployeeUser
from .models import User, Influencer, Brand, Employee 
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated 
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from djoser.serializers import TokenCreateSerializer
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()

class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")

class InfluencerSignupView(generics.GenericAPIView):
    serializer_class = InfluencerSignupSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email to user
        email_data = {
            'email_subject': 'Verify your email',
            'email_body': f"Hello {user.username},\n\nPlease click on the link below to verify your email address:\nhttp://{request.get_host()}/api/verify-email/?etoken={user.email_verification_token}",
            'to_email': user.email
        }
        Util.send_email(email_data)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Account created successfully"
        })


class BrandSignupView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = BrandSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email to user
        email_data = {
            'email_subject': 'Verify your email',
            'email_body': f"Hello {user.username},\n\nPlease click on the link below to verify your email address:\nhttp://{request.get_host()}/api/verify-email/?etoken={user.email_verification_token}",
            'to_email': user.email
        }
        Util.send_email(email_data)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Account created successfully"
        })


class EmployeeSignupView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = EmployeeSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email to user
        email_data = {
            'email_subject': 'Verify your email',
            'email_body': f"Hello {user.username},\n\nPlease click on the link below to verify your email address:\nhttp://{request.get_host()}/api/verify-email/?etoken={user.email_verification_token}",
            'to_email': user.email
        }
        Util.send_email(email_data)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Account created successfully"
        })


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        etoken = request.GET.get('etoken')
        try:
            payload = jwt.decode(etoken, settings.SECRET_KEY)
            user= User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

                # Send verification email
                email_subject = 'Verify Your Email'
                email_body = render_to_string('verify_email.html', {'user': user})
                email = EmailMessage(email_subject, email_body, to=[user.email])
                email.send()

            return Response({
                "user":UserSerializer(user, context=self.get_serializer_context()).data,
                "token":Token.objects.get(user=user).key,
                "message":"account created successfully"
            })
        except:
            pass

    
class CustomAuthToken(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # determine the user's dashboard URL based on their user type
        if hasattr(user, 'influencer'):
            dashboard_url = f"/{user.username}-dashboard/"
        elif hasattr(user, 'brand'):
            dashboard_url = f"/{user.username}-dashboard/"
        elif hasattr(user, 'employee'):
            dashboard_url = f"/{user.username}-dashboard/"
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'dashboard_url': dashboard_url
        })


class UserDashboardView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_type = user.user_type
        if user_type == 'influencer':
            influencer = Influencer.objects.get(user=user)
            data = {
                'username': user.username,
                'user_type': user_type,
                'name': influencer.name,
                'email': user.email,
                'profile_picture': influencer.profile_picture.url,
                'social_media_links': influencer.social_media_links,
                'stats': {
                    'followers': influencer.followers,
                    'following': influencer.following,
                    'posts': influencer.posts.count()
                }
            }
        elif user_type == 'brand':
            brand = Brand.objects.get(user=user)
            data = {
                'username': user.username,
                'user_type': user_type,
                'name': brand.name,
                'email': user.email,
                'profile_picture': brand.profile_picture.url,
                'website': brand.website,
                'stats': {
                    'followers': brand.followers.count(),
                    'following': brand.following.count(),
                    'campaigns': brand.campaigns.count()
                }
            }
        else:
            employee = Employee.objects.get(user=user)
            data = {
                'username': user.username,
                'user_type': user_type,
                'name': employee.name,
                'email': user.email,
                'profile_picture': employee.profile_picture.url,
                'position': employee.position,
                'department': employee.department,
            }
        return Response(data)
 
class LogoutView(APIView):
    
    def get_queryset(self):
        return User.objects.all()

    def post(self, request, format=None):
        request.auth.delete()
        return redirect('/')


class BrandOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated,IsBrandUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user


class InfluencerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated,IsInfluencerUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
        

class EmployeeOnlyView(generics.RetrieveAPIView):
    
    permission_classes=[permissions.IsAuthenticated,IsEmployeeUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user


class DeleteAccountView(APIView):

    def get_queryset(self):
        return User.objects.all()
    
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })

'''
class GetUserProfileView(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            user_profile = User.objects.get(user=user)
            user_profile = UserSerializer(user_profile)

            return Response({ 'profile': user_profile.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' })

'''

class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandProfileSerializer

class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandProfileSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeProfileSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeProfileSerializer


class InfluencerListCreateView(generics.ListCreateAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerProfileSerializer

class InfluencerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerProfileSerializer


class UpdateProfilePicView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePictureUpdateSerializer

class UpdateProfilePicViewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePictureUpdateSerializer


#Need this for chat function

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    # other viewset logic

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def all(self, request):
        serializer = UserSerializer(
            User.objects.all(), many=True, context={"request": request}
        )
        

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    def get_queryset(self):
        return User.objects.all()
   
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            
            # Send email notification
            subject = 'Password Change Notification'
            html_message = render_to_string('password_change_email.html', {'user': self.object})
            plain_message = strip_tags(html_message)
            from_email = 'stratifi8@gmail.com'
            to_email = self.object.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            # Re-authenticate the user to keep them logged in
            update_session_auth_hash(request, self.object)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = get_object_or_404(User, email=email)

        # Create password reset token and email it to the user
        current_site = get_current_site(request)
        subject = "Reset your password"
        message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
                "reset_url": reverse(
                    "reset-password-confirm", args=[user.pk, default_token_generator.make_token(user)]
                ),
            },
        )

        email = EmailMessage(
            subject=subject,
            body=message,
            to=[email],
        )
        email.send()

        return Response(
            {"success": "Password reset email has been sent."},
            status=status.HTTP_200_OK,
        )


#check this out
class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()

