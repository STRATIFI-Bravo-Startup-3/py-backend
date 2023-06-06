from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super(CustomAccountAdapter, self).save_user(request, user, form, commit)
        user.role = form.cleaned_data.get("role")
        if user.role == User.Role.INFLUENCER:
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
        if user.role == User.Role.BRAND:
            user.company_name = f"{user.first_name} {user.last_name}"
        user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(CustomSocialAccountAdapter, self).save_user(
            request, sociallogin, form
        )
        user.role = request.data.get("role")
        if user.role == User.Role.INFLUENCER:
            user.first_name = sociallogin.account.extra_data.get("first_name")
            user.last_name = sociallogin.account.extra_data.get("last_name")
        if user.role == User.Role.BRAND:
            user.company_name = f"{user.first_name} {user.last_name}"
        user.save()
        return user


# class CustomAccountAdapter(DefaultAccountAdapter):
#     def save_user(self, request, user, form, commit=False):
#         user = super().save_user(request, user, form, commit)
#         user.role = form.cleaned_data.get('role')
#         user.save()
#         return user


# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def save_user(self, request, sociallogin, form=None):
#         user = super().save_user(request, sociallogin, form)
#         user.role = request.data.get('role')
#         user.save()
#         return user
