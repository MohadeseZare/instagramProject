from rest_framework import permissions


class InstagramPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.instagram_user_id:
            return True
