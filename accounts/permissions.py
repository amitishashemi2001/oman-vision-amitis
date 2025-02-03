from rest_framework.permissions import BasePermission

class IsExpertUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_active and not request.user.is_staff and not request.user.is_superuser)
