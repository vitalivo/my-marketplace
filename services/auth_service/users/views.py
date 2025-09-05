from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import Profile
from .serializers import ProfileSerializer

# -------------------------------
# 1️⃣ Health‑эндпоинт (для /api/health/)
# -------------------------------
class HealthView(APIView):
    """
    Самый простой «ping»‑эндпоинт.
    Возвращает JSON {"status":"ok"} и статус 200.
    """
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


# -------------------------------
# 2️⃣ Profile ViewSet
# -------------------------------
class ProfileViewSet(viewsets.ModelViewSet):
    """
    GET    /api/profile/          – список (в нашем случае один элемент)
    PATCH  /api/profile/<pk>/    – частичное обновление профиля
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пользователь видит только свой профиль
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)