from rest_framework.permissions import BasePermission


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if self.request.user.user_type == 'provider':
            return True
        return False
