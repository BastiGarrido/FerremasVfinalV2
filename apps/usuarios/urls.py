from django.urls import path
from .views import RegisterView, LoginView

app_name = 'usuarios_api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
]