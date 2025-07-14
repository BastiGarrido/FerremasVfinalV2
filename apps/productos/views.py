from rest_framework import viewsets, status, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsBodeguero, IsVendedorOrAdmin

class ProductViewSet(viewsets.ModelViewSet):
    """
    Gestión de productos:
    - list            GET    /api/productos/
    - create          POST   /api/productos/
    - retrieve        GET    /api/productos/{id}/
    - update          PUT    /api/productos/{id}/
    - partial_update  PATCH  /api/productos/{id}/
    - destroy         DELETE /api/productos/{id}/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # filtros, búsqueda y ordenamiento
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'brand': ['exact'],
        'category': ['exact'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action == 'create':
            # Solo bodeguero puede crear productos
            permission_classes = [IsBodeguero]
        elif self.action in ('update', 'partial_update', 'destroy'):
            # Solo vendedor o admin puede modificar/eliminar
            permission_classes = [IsVendedorOrAdmin]
        else:
            # list y retrieve abiertos a todos
            permission_classes = [AllowAny]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        # Al listar, sólo mostrar los publicados
        if self.action == 'list':
            return Product.objects.filter(is_published=True)
        return super().get_queryset()

    def perform_create(self, serializer):
        # Al crear, precio inicial 0 y publicado en False
        serializer.save(price=0, is_published=False)