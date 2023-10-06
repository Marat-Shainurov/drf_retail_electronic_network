from rest_framework import permissions


class IsUserActive(permissions.BasePermission):
    message = 'Inactive user'

    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        return False
