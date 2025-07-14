from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('catalogo/', TemplateView.as_view(template_name='catalogo.html'),name='catalogo'),
    path('nosotros/',TemplateView.as_view(template_name='nosotros.html'), name='nosotros'),
    path('contacto/',TemplateView.as_view(template_name='contacto.html'), name='contacto'),
    path('carrito/',  TemplateView.as_view(template_name='carrito.html'),  name='carrito'),
    path('pedidos/',  TemplateView.as_view(template_name='pedidos.html'),  name='mis_pedidos'),
    path('pago/<int:pk>/', TemplateView.as_view(template_name='pago.html'), name='pago'),

    # API endpoints grouped by app
    path('api/usuarios/', include(('apps.usuarios.urls','usuarios_api'), namespace='usuarios_api')),
    path('api/productos/', include('apps.productos.urls')),
    path('api/carrito/', include('apps.carrito.urls')),
    path('api/pedidos/', include('apps.pedidos.urls')),
    path('api/pagos/', include('apps.pagos.urls')),

    # ——— aquí agregas los dashboards ———
    path('vendedor/dashboard/',TemplateView.as_view(template_name='vendedor_dashboard.html'),name='vendedor_dashboard'),
    path('bodeguero/dashboard/',TemplateView.as_view(template_name='bodeguero_dashboard.html'),name='bodeguero_dashboard'),
    path('contador/dashboard/',TemplateView.as_view(template_name='contador_dashboard.html'),name='contador_dashboard'),
    path('administrador/dashboard/',TemplateView.as_view(template_name='administrador_dashboard.html'),name='administrador_dashboard'),
]
