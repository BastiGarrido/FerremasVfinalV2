# apps/pagos/models.py

from django.db import models
from apps.usuarios.models import UserProfile
from apps.pedidos.models import Order

class PaymentTransaction(models.Model):
    order      = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='transaction')
    user       = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount     = models.DecimalField(max_digits=12, decimal_places=2)
    token      = models.CharField(max_length=100, unique=True)
    url        = models.URLField()
    status     = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transacción {self.token} ({self.status})"