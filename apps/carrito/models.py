from django.db import models
from apps.usuarios.models import UserProfile
from apps.productos.models import Product

class CartItem(models.Model):
    user       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity   = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.uid} – {self.product.name} x{self.quantity}"