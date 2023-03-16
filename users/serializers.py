from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django_countries.serializers import CountryFieldMixin
from .models import User, Influencer, Brand, Employee
from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['id', 'username', 'email','is_brand',  'is_influencer', 'is_employee', 
        #'slug'
        ]
        #lookup_field = 'slug'

class InfluencerSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        # Add UniqueValidator for username
        username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            is_influencer=True,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        user.set_password(password)
        user.save()
        Token.objects.get_or_create(user=user)
        Influencer.objects.create(user=user)
        return user


class BrandSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        # Add UniqueValidator for username
        username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            is_brand=True,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        user.set_password(password)
        user.save()
        Token.objects.get_or_create(user=user)
        Brand.objects.create(user=user)
        return user



class EmployeeSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        # Add UniqueValidator for username
        username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            is_employee=True,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        user.set_password(password)
        user.save()
        Token.objects.get_or_create(user=user)
        Brand.objects.create(user=user)
        return user


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
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new password and confirm password do not match.")
        return data


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    username_or_email = serializers.CharField(
        label=_("Username or Email"), max_length=254
    )

    def validate_username_or_email(self, value):
        """
        Validate that the username or email exists in the system.
        """
        user_model_field = User.USERNAME_FIELD
        try:
            user = User.objects.get(**{user_model_field: value})
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _("User with this username/email does not exist.")
            )
        return user

    def save(self):
        """
        Generate a one-use only link for resetting password and send it to the user.
        """
        request = self.context.get("request")
        user = self.validated_data["username_or_email"]
        form = PasswordResetForm({"email": user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name="registration/password_reset_email.html",
                subject_template_name="registration/password_reset_subject.txt",
            )