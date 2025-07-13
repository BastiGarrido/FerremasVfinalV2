from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('administrador', 'Administrador'),
        ('cliente',       'Cliente'),
        ('contador',      'Contador'),
        ('bodeguero',     'Bodeguero'),
        ('vendedor',      'Vendedor'),
    ]
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"