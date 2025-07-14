from django.db import models

class Product(models.Model):
    name          = models.CharField("Nombre", max_length=100)
    description   = models.TextField("Descripción", blank=True)
    brand         = models.CharField("Marca", max_length=50, blank=True)       # Nuevo
    category      = models.CharField("Categoría", max_length=50, blank=True)   # Nuevo
    price         = models.DecimalField(
        "Precio",
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True
    )  # Ahora default=0, editable solo por vendedor/admin
    stock         = models.PositiveIntegerField("Stock disponible", default=0)
    image_url     = models.URLField("URL de imagen", blank=True)
    is_published  = models.BooleanField(
        "Publicado en catálogo",
        default=False,
        help_text="Sólo los productos publicados aparecen en el catálogo"
    )  # Nuevo
    created_at    = models.DateTimeField("Creado en", auto_now_add=True)
    updated_at    = models.DateTimeField("Modificado en", auto_now=True)

    def __str__(self):
        return f"{self.name} (${self.price})"