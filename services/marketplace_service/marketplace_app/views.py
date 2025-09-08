from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework import viewsets, permissions
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer

# -----------------------------------------------------------------
#  Категории – только чтение, публичные
# -----------------------------------------------------------------
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]   # публично

# -----------------------------------------------------------------
#  Товары – CRUD + поиск по радиусу
# -----------------------------------------------------------------
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        # Параметры поиска: lat, lon, radius (км)
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius')

        if lat and lon and radius:
            user_point = Point(float(lon), float(lat), srid=4326)
            qs = qs.annotate(
                distance=Distance('location', user_point)
            ).filter(distance__lte=float(radius) * 1000)   # km → meters
        return qs

    def perform_create(self, serializer):
        # Привязываем текущего пользователя как владельца
        serializer.save(owner=self.request.user)