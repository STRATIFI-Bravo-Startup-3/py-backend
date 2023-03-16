from rest_framework.permissions import BasePermission
from rest_framework import permissions

edit_methods = ("PUT", "PATCH", "POST")
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsBrandUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_brand)


class IsInfluencerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_influencer)


class IsEmployeeUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee and request.user.is_staff and request.user.is_admin)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsEmployeeUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_employee)



class IsInfluencerUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_influencer)


class IsBrandUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or (request.user and request.user.is_brand))

        
class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)


class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
