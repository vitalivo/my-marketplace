import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    """Клиент DRF, без авторизации."""
    return APIClient()

@pytest.fixture
def auth_header(db):
    """
    Фикстура, создающая тестового пользователя и возвращающая заголовок
    Authorization: Bearer <access_token>
    """
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass')
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'}