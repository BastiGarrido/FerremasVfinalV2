from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    - list:      GET    /api/pedidos/
    - create:    POST   /api/pedidos/        ← genera pedido desde el carrito
    - retrieve:  GET    /api/pedidos/{id}/
    - destroy:   DELETE /api/pedidos/{id}/
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Historial de pedidos del usuario
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        cart_items = user.cart_items.all()
        if not cart_items.exists():
            raise ValidationError("El carrito está vacío.")
        total = sum(item.product.price * item.quantity for item in cart_items)
        # Crea el pedido
        order = serializer.save(user=user, total=total)
        # Genera OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Vacía el carrito
        cart_items.delete()