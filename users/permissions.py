from rest_framework.permissions import BasePermission
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model


class IsBrandUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.Role.BRAND)


class IsInfluencerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.Role.INFLUENCER)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsInfluencerUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or (request.user and request.user.role == User.Role.INFLUENCER))

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.role == User.Role.INFLUENCER)


class IsBrandUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or (request.user and request.user.role == User.Role.BRAND))

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.role == User.Role.BRAND)


class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)


class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
