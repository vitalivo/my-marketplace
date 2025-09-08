from django.db import models
from django.contrib.gis.db import models as gis_models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Гео‑поле: хранит координаты (lon, lat) в системе EPSG:4326
    location = gis_models.PointField()

    category = models.ForeignKey(
        Category,
        related_name="items",
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="items",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title