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
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Usa el perfil de usuario para obtener los pedidos
        profile = self.request.user.profile
        return Order.objects.filter(user=profile)

    def perform_create(self, serializer):
        # Obtén el perfil del usuario
        profile = self.request.user.profile
        # Obtén los items del carrito asociados al perfil
        from apps.carrito.models import CartItem
        cart_items = CartItem.objects.filter(user=profile)
        # Calcula el total sumando cada item
        total = sum([item.product.price * item.quantity for item in cart_items])
        # Crea el pedido con user=profile y total
        order = serializer.save(user=profile, total=total)
        # Luego asocia los items al pedido (si tu modelo lo necesita)
        for item in cart_items:
            order.items.add(item)
        # Opcional: vaciar el carrito después de crear pedido
        cart_items.delete()
