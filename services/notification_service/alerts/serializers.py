from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Alert


User = get_user_model()          # будет django.contrib.auth.models.User


class UserSerializer(serializers.ModelSerializer):
    """
    Минимальный набор полей, который будет возвращаться в ответах.
    При необходимости добавляй дополнительные read‑only поля (email, first_name и т.д.).
    """
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("id", "username", "email")


class AlertSerializer(serializers.ModelSerializer):
    """
    Вложенный `user`‑объект только для чтения.
    При создании/обновлении Alert пользователь берётся из request.user
    (см. view‑set), поэтому поле объявлено `read_only=True`.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ("id", "title", "message", "created_at", "is_read", "user")
        read_only_fields = ("id", "created_at", "user")