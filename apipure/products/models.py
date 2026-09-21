from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField("nombre", max_length=150)
    description = models.TextField("descripción", blank=True)
    price = models.DecimalField(
        "precio", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField("existencias", default=0)
    active = models.BooleanField("activo", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
