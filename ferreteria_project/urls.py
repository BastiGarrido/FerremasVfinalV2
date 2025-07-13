from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('admin/', admin.site.urls),

    # API endpoints grouped by app
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('api/productos/', include('apps.productos.urls')),
    path('api/carrito/', include('apps.carrito.urls')),
    path('api/pedidos/', include('apps.pedidos.urls')),
    path('api/pagos/', include('apps.pagos.urls')),
]
