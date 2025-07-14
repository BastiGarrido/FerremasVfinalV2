from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, AdminUserViewSet

app_name = 'usuarios_api'

router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('', include(router.urls)),
]