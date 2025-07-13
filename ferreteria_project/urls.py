
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.usuarios.urls')),
    path('api/', include('apps.productos.urls')),
    path('api/', include('apps.carrito.urls')),
    path('api/', include('apps.pedidos.urls')),
    path('api/', include('apps.pagos.urls')),
    # luego agregaremos los demás apps aquí
]
