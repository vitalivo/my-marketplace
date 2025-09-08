import pytest

@pytest.mark.django_db
def test_health_endpoint(api_client):
    """Эндпоинт /api/health/ должен возвращать {'status':'ok'}."""
    response = api_client.get('/api/health/')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.django_db
def test_profile_endpoint(api_client, auth_header):
    """Проверяем, что авторизованный запрос к /api/profile/ возвращает профиль."""
    response = api_client.get('/api/profile/', **auth_header)
    assert response.status_code == 200
    # Должен быть массив с одним объектом (профиль текущего пользователя)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    profile = data[0]
    # Поля, которые определены в модели Profile
    assert "phone_number" in profile
    assert "role" in profile
    assert "photo" in profile