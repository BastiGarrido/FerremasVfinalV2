from rest_framework import permissions

class IsBodegueroOrAdmin(permissions.BasePermission):
    """
    Permite sólo a los usuarios con rol 'bodeguero' o superusuarios (is_staff/is_superuser) crear.
    """
    def has_permission(self, request, view):
        # Siempre permitir GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Para acciones no seguras (POST, PUT, DELETE...)
        user = request.user
        # superuser o staff?
        if user.is_superuser or user.is_staff:
            return True

        # role desde tu UserProfile (related_name 'profile')
        profile = getattr(user, 'profile', None)
        if profile and profile.role == 'bodeguero':
            return True

        return False