from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # Solo el propio usuario
    def get_queryset(self):
        return UserProfile.objects.filter(uid=self.request.user.uid)

    # Endpoint adicional /api/usuarios/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = UserProfile.objects.get(uid=request.user.uid)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
