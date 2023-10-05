from django.db import models

from app.core.models import TimeStampedMixin


class Brand(TimeStampedMixin):
    name = models.CharField()
    description = models.CharField()

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Product(TimeStampedMixin):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="product_brand"
    )
    name = models.CharField()
    description = models.CharField()
    sku = models.CharField(unique=True)
    price = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
