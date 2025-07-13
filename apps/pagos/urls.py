from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

router = DefaultRouter()
# Registramos sin prefix para que las rutas de acción queden en /api/pagos/initiate/ etc.
router.register('', PaymentViewSet, basename='pago')

urlpatterns = router.urls