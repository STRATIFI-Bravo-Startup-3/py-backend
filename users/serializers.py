from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django_countries.serializers import CountryFieldMixin
from .models import User, Influencer, Brand, Employee
from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model=User
        fields=['username', 'email','is_brand',  'is_influencer', 'is_employee']

class InfluencerSignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User

        fields=['username','email', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def create(self, validated_data, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_influencer=True
        user.save()
        Token.objects.get_or_create(user=user)
        Influencer.objects.create(user=user)
        return user

class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def create(self, validated_data, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        #password2=self.validated_data['password2']
        #if password !=password2:
        #    raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_influencer=True
        user.save()
        Token.objects.get_or_create(user=user)
        Influencer.objects.create(user=user)
        return user


class BrandSignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    

    def create(self, validated_data, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_brand=True
        user.save()
        Token.objects.get_or_create(user=user)
        Brand.objects.create(user=user)
        return user


class EmployeeSignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    

    def create(self, validated_data, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_employee=True
        user.is_admin=True
        user.is_staff=True
        user.save()
        Token.objects.get_or_create(user=user)
        Employee.objects.create(user=user)
        return user




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



class BrandProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class InfluencerProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Influencer
        fields = '__all__'

class EmployeeProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_pic']

        


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)