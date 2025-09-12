import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Стандартная модель пользователя, которую Django использует в проекте
from django.contrib.auth import get_user_model
User = get_user_model()


@pytest.fixture
def user(db):
    """
    Фикстура, создающая тестового пользователя.
    """
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass",
    )


@pytest.fixture
def api_client():
    """
    Фикстура, возвращающая чистый API‑клиент.
    Аутентификация будет выполнена в каждом тесте через
    `client.force_authenticate(user=…)`.
    """
    return APIClient()


def test_health_endpoint(api_client, user):
    """
    Проверяем публичный health‑чек.
    По умолчанию в `settings.py` у вас включена аутентификация,
    поэтому в тесте принудительно аутентифицируем клиента.
    """
    api_client.force_authenticate(user=user)

    url = reverse("health")          # имя, указанное в @api_view
    resp = api_client.get(url)

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": "ok"}


def test_create_alert(api_client, user):
    """
    Тестируем создание нового оповещения через ViewSet.
    """
    api_client.force_authenticate(user=user)

    url = reverse("alert-list")      # имя, генерируемое DRF‑router
    data = {
        "title": "Тестовое оповещение",
        "message": "Привет, мир!",
    }

    resp = api_client.post(url, data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED

    payload = resp.json()
    # Проверяем, что сериализатор вернул ожидаемые поля
    assert payload["title"] == data["title"]
    assert payload["message"] == data["message"]
    assert payload["is_read"] is False
    assert payload["user"]["username"] == user.username
    assert payload["user"]["email"] == user.email