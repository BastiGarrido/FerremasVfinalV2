from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['uid', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['uid', 'email', 'created_at', 'updated_at']