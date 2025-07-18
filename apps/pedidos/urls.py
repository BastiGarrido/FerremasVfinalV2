from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'pedidos', OrderViewSet, basename='pedido')

urlpatterns = router.urls