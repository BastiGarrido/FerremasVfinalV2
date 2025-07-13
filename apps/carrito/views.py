from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.decorators import action 

class CartItemViewSet(viewsets.ModelViewSet):
    """
    Gestión de carrito:
    - list    GET    /api/carrito/carrito/
    - create  POST   /api/carrito/carrito/
    - retrieve GET   /api/carrito/carrito/{id}/
    - update  PUT    /api/carrito/carrito/{id}/
    - partial_update PATCH /api/carrito/carrito/{id}/
    - destroy DELETE /api/carrito/carrito/{id}/
    - clear   DELETE /api/carrito/carrito/clear/  (si tienes action)
    """
    serializer_class   = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        return CartItem.objects.filter(user=profile)

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(user=profile)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        Vacía todo el carrito del usuario autenticado.
        """
        profile = request.user.profile
        CartItem.objects.filter(user=profile).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)