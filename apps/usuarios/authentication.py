from rest_framework import authentication, exceptions
from firebase_admin import auth as firebase_auth
from .models import UserProfile

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header:
            return None

        parts = header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise exceptions.AuthenticationFailed('Encabezado Authorization inválido')

        id_token = parts[1]
        try:
            decoded = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Token de Firebase inválido')

        uid = decoded['uid']
        # Obtener o crear perfil local
        profile, _ = UserProfile.objects.get_or_create(
            uid=uid,
            defaults={'email': decoded.get('email', '')}
        )
        return (profile, None)