from rest_framework import permissions

class IsBodeguero(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        profile = getattr(user, 'profile', None)
        return profile and profile.role == 'bodeguero'

class IsVendedorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        profile = getattr(user, 'profile', None)
        return profile and profile.role == 'vendedor'
