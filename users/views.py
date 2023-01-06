from django.http import request
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import (DemoSerializer, InfluencerSignupSerializer, 
EmployeeSignupSerializer, BrandSignupSerializer, InfluencerProfileSerializer,
BrandProfileSerializer, EmployeeProfileSerializer, ProfilePictureUpdateSerializer,
UserSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsBrandUser, IsInfluencerUser, IsEmployeeUser
from .models import User, Influencer, Brand, Employee 
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404


class InfluencerSignupView(generics.GenericAPIView):
    serializer_class=InfluencerSignupSerializer
    authentication_classes=()
    permission_classes=()
    def get_queryset(self):
        return Influencer.objects.all()

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })

class DemoSignupView(generics.GenericAPIView):
    serializer_class=InfluencerSignupSerializer
    authentication_classes=()
    permission_classes=()
    def get_queryset(self):
        return Influencer.objects.all()

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()


        user_data = serializer.data
        user=User.objects.get(email=user_data['email'])
        etoken = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        absurl = 'https://' + current_site + relativeLink + '?etoken='+str(etoken)
        email_body = 'Hi'+user.username + 'use the link below to verify your email \n' + absurl

        data={
            'email_body':email_body,
            'to_email':user.email,
            'email_subject':'Verifiy your Email'
        }
        Util.send_email(data)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        etoken = request.GET.get('etoken')
        try:
            payload = jwt.decode(etoken, settings.SECRET_KEY)
            user= User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({
                "user":UserSerializer(user, context=self.get_serializer_context()).data,
                "token":Token.objects.get(user=user).key,
                "message":"account created successfully"
            })
        except:
            pass
        '''except jwt.ExpiredSignatureError  as identifier:
            return Response(['error':'Activtion expired'], status=status.HTTP_400_BAD_REQUEST)
        except jwt.exception.DecodeError  as identifier:
            return Response(['error':'Invalid Token'], status=status.HTTP_400_BAD_REQUEST)
'''

class BrandSignupView(generics.GenericAPIView):
    authentication_classes=()
    permission_classes=()
    serializer_class=BrandSignupSerializer
    def get_queryset(self):
        return Brand.objects.all()

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })

class EmployeeSignupView(generics.GenericAPIView):
    authentication_classes=()
    permission_classes=()
    serializer_class=EmployeeSignupSerializer
    def get_queryset(self):
        return Employee.objects.all()

    serializer_class=EmployeeSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })
    
class CustomAuthToken(ObtainAuthToken):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
 

class LogoutView(APIView):
    
    def get_queryset(self):
        return User.objects.all()

    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class BrandOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsBrandUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user


class InfluencerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsInfluencerUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
        

class EmployeeOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsEmployeeUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user


#class DeleteAccountView(APIView):
class DeleteAccountView(generics.RetrieveUpdateAPIView):

    def get_queryset(self):
        return User.objects.all()
    
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })


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
