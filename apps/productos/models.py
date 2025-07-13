from django.db import models

class Product(models.Model):
    name        = models.CharField("Nombre", max_length=100)
    description = models.TextField("Descripción", blank=True)
    price       = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField("Stock disponible", default=0)
    image_url   = models.URLField("URL de imagen", blank=True)
    created_at  = models.DateTimeField("Creado en", auto_now_add=True)
    updated_at  = models.DateTimeField("Modificado en", auto_now=True)

    def __str__(self):
        return f"{self.name} (${self.price})"