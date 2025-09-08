import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    """Создаёт и возвращает обычного пользователя."""
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def auth_header(test_user):
    """
    Возвращает:
    - HTTP‑заголовок с JWT,
    - объект пользователя (чтобы тесты могли обратиться к нему напрямую).
    """
    token = RefreshToken.for_user(test_user)
    return {
        "HTTP_AUTHORIZATION": f"Bearer {token.access_token}",
        "user": test_user,          # <-- добавляем объект пользователя
    }