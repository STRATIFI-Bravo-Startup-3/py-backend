from rest_framework.permissions import BasePermission



class IsBrandUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_brand)


class IsInfluencerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_influencer)


class IsEmployeeUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_employee and request.user.is_staff and request.user.is_admin)