from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from django.db import IntegrityError

class CartItemViewSet(viewsets.ModelViewSet):
    """
    - list:    GET    /api/carrito/
    - create:  POST   /api/carrito/        (product, quantity)
    - retrieve: GET   /api/carrito/{id}/
    - update:   PUT   /api/carrito/{id}/
    - partial_update: PATCH /api/carrito/{id}/
    - destroy: DELETE /api/carrito/{id}/
    - empty:    DELETE /api/carrito/empty/  (vaciar carrito)
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        qty = serializer.validated_data['quantity']
        item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            item.quantity += qty
            item.save()
        else:
            serializer.save(user=user)

    @action(detail=False, methods=['delete'], url_path='empty')
    def empty(self, request):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        user    = self.request.user
        product = serializer.validated_data['product']
        qty     = serializer.validated_data['quantity']
        try:
            # Intento de creación normal
            serializer.save(user=user)
        except IntegrityError:
            # Si ya existe, la inserción falla: actualizo la cantidad
            item = CartItem.objects.get(user=user, product=product)
            item.quantity += qty
            item.save()