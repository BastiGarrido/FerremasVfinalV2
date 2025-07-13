from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Gestión de productos:
    - list      GET    /api/productos/
    - create    POST   /api/productos/
    - retrieve  GET    /api/productos/{id}/
    - update    PUT    /api/productos/{id}/
    - partial_update PATCH /api/productos/{id}/
    - destroy   DELETE /api/productos/{id}/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

