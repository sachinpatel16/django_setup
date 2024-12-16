from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.permissions import SAFE_METHODS, BasePermission


class SimplePermission(BasePermission):
    """
    Simple permission to prevent code duplication in has_permission & has_object_permission
    """

    def has_access(self, request, view, instance=None):
        raise NotImplementedError

    def has_permission(self, request, view):
        return self.has_access(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_access(request, view, instance=obj)

    class Meta:
        abstract = True


class IsReadAction(SimplePermission):
    def has_access(self, request, view, instance=None):
        return request.method in SAFE_METHODS


IsEditAction = ~IsReadAction


class IsAPIKEYAuthenticated(BasePermission):
    """
    This permission class is used for check api key and identify the requests.
    """

    def has_permission(self, request, view):
        # API_KEY should be in request headers to authenticate requests
        api_key_secret = request.META.get("HTTP_API_KEY")
        try:
            api_key_secret = bytes(api_key_secret, "utf-8")
        except TypeError:
            raise ParseError("API-KEY is required.")
        if api_key_secret == settings.API_KEY_SECRET:
            return True
        else:
            raise ParseError("Invalid API-KEY.")


# from rest_framework import permissions


class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is a student
        return request.user.user_type == "student"


class IsSuperAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is a admin
        return request.user.user_type.type == "admin"
