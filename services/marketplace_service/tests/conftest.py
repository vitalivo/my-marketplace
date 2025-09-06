import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    """Клиент DRF без авторизации."""
    return APIClient()

@pytest.fixture
def auth_header(db):
    """Создаёт тестового пользователя и возвращает JWT‑заголовок."""
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpass")
    token = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {token.access_token}"}