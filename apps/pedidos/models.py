from django.db import models
from apps.usuarios.models import UserProfile
from apps.productos.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING',   'Pendiente'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]
    user       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.user.uid} - {self.status}"

class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity   = models.PositiveIntegerField()
    price      = models.DecimalField(max_digits=10, decimal_places=2)  # precio al momento del pedido

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (${self.price})"