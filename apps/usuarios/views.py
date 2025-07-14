# apps/usuarios/views.py

from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import RegisterSerializer, UserSerializer

 # Exime CSRF de toda la clase
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registro de usuarios:
    - POST /api/usuarios/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.profile.role
            },
            "token": token.key
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(ObtainAuthToken):
    """
    Endpoint para login de usuarios:
    - POST /api/usuarios/login/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data.get('token')
        token     = Token.objects.get(key=token_key)
        user      = token.user
        role      = user.profile.role
        return Response({
            "token": token_key,
            "user": {
                "username": user.username,
                "role": role
            }
        }, status=status.HTTP_200_OK)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Sólo superusuarios pueden listar, ver, actualizar o borrar usuarios.
    DELETE /api/usuarios/admin/users/{id}/
    """
    queryset = User.objects.all().select_related('profile')
    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAdminUser]