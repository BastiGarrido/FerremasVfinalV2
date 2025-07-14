from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registro de usuarios:
    - POST /api/usuarios/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Validar y crear el usuario
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generar o recuperar token de autenticación
        token, _ = Token.objects.get_or_create(user=user)

        # Devolver JSON con datos de usuario y token
        return Response(
            {
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.profile.role  # related_name='profile' :contentReference[oaicite:3]{index=3}
                },
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(ObtainAuthToken):
    """
    Endpoint para login de usuarios:
    - POST /api/usuarios/login/
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Llamamos a ObtainAuthToken para validar credenciales y crear token
        response = super().post(request, *args, **kwargs)
        token_key = response.data.get('token')

        # Recuperamos el usuario y su rol
        token = Token.objects.get(key=token_key)
        user = token.user
        role = user.profile.role  # related_name='profile' :contentReference[oaicite:4]{index=4}

        # Devolvemos token + info de usuario
        return Response(
            {
                "token": token_key,
                "user": {
                    "username": user.username,
                    "role": role
                }
            },
            status=status.HTTP_200_OK
        )