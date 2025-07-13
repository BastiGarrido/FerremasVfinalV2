from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r'carrito', CartItemViewSet, basename='carrito')

urlpatterns = router.urls