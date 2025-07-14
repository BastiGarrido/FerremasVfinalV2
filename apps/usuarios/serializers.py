from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='userprofile.role')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    email    = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    role     = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        default='cliente'
    )

    class Meta:
        model  = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        # Extraemos el rol antes de crear el usuario
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Creamos el perfil con el rol
        UserProfile.objects.create(user=user, role=role)
        return user