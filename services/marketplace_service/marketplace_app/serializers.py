from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from django.contrib.gis.measure import Distance  # уже импортирован
from .models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ItemSerializer(GeoFeatureModelSerializer):
    """
    GeoFeatureModelSerializer:
    • возвращает Feature (geometry + properties);
    • поле `location` объявлено как GeometryField → принимает GeoJSON‑dict.
    """
    distance = serializers.SerializerMethodField(read_only=True)
    location = GeometryField()          # <-- важный момент: преобразуем GeoJSON → Point

    class Meta:
        model = Item
        geo_field = "location"
        fields = (
            "id",
            "title",
            "description",
            "price",
            "location",
            "category",
            "owner",
            "created_at",
            "distance",
        )
        read_only_fields = ("owner", "created_at", "distance")

    # -----------------------------------------------------------------
    #  Преобразуем объект Distance в обычный float (км) и **перезаписываем**
    #  атрибут, чтобы он не попал в сериализованный output ещё раз.
    # -----------------------------------------------------------------
    def get_distance(self, obj):
        if hasattr(obj, "distance"):
            # Если это django.contrib.gis.measure.Distance → берём km
            if isinstance(obj.distance, Distance):
                # Перезаписываем атрибут, чтобы drf‑gis не вывел оригинал
                obj.distance = round(obj.distance.km, 2)
                return obj.distance
            # Если уже число (например, в тесте без аннотации)
            return obj.distance
        return None