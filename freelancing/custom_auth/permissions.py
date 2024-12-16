from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # return obj.user == request.user
        return request.user.user_type.type == "admin"
