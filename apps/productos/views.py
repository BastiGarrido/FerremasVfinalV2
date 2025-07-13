from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
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

    # Configuración de filtros, búsqueda y ordenamiento
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'price': ['gte', 'lte'],    # Filtrar por rango de precio
        'brand': ['exact'],          # Filtrar por marca
        'category': ['exact'],       # Filtrar por categoría
    }
    search_fields = ['name', 'description']  # Búsqueda de texto en nombre o descripción
    ordering_fields = ['price', 'name', 'created_at']  # Campos para ordenar
    ordering = ['name']  # Orden por defecto (ascendente por nombre)