from django.db import models

class UserProfile(models.Model):
    uid = models.CharField(max_length=128, unique=True)
    email = models.EmailField(blank=True)
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('contador', 'Contador'),
        ('bodeguero', 'Bodeguero'),
        ('vendedor', 'Vendedor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uid} ({self.role})"

    @property
    def is_authenticated(self):
        # DRF lo usa para saber si el usuario "está logueado"
        return True

    @property
    def is_anonymous(self):
        # No es un usuario anónimo
        return False
