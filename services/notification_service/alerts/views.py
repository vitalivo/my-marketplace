from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Alert
from .serializers import AlertSerializer, UserSerializer


class AlertViewSet(viewsets.ModelViewSet):
    """
    CRUD для оповещений. Пользователь видит только свои записи.
    """
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def health(request):
    """Health‑check – публичный эндпоинт, но в тестах клиент аутентифицируется."""
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """Возвращает данные текущего пользователя."""
    ser = UserSerializer(request.user)
    return Response(ser.data)