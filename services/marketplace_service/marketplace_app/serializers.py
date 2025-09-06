from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ItemSerializer(GeoFeatureModelSerializer):
    """
    GeoFeatureModelSerializer автоматически:
    • принимает GeoJSON (dict) в поле `location`;
    • выводит GeoJSON с полем `geometry`;
    • добавляет свойства (`properties`) – остальные поля модели.
    """
    distance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        geo_field = "location"               # <-- указываем, какая колонка хранит гео‑данные
        fields = (
            "id",
            "title",
            "description",
            "price",
            "location",      # будет возвращаться как GeoJSON
            "category",
            "owner",
            "created_at",
            "distance",
        )
        read_only_fields = ("owner", "created_at", "distance")

    def get_distance(self, obj):
        # Если в view‑set будет аннотировано поле `distance`,
        # возвращаем его, иначе None.
        return getattr(obj, "distance", None)