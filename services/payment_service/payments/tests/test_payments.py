import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from payments.models import Payment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def auth_header(test_user):
    token = RefreshToken.for_user(test_user)
    return {
        "HTTP_AUTHORIZATION": f"Bearer {token.access_token}",
        "user": test_user,
    }


@pytest.mark.django_db
def test_create_payment(api_client, auth_header, test_user):
    payload = {
        "amount": "10.00",
        "currency": "usd",
        "success_url": "https://example.com/success/",
        "cancel_url": "https://example.com/cancel/",
    }
    resp = api_client.post(
        "/api/payments/",
        payload,
        format="json",
        **auth_header,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "checkout_url" in data
    assert "payment_id" in data

    # Проверяем, что запись в базе действительно появилась
    payment = Payment.objects.get(id=data["payment_id"])
    assert payment.user == test_user
    assert float(payment.amount) == 10.00
    assert payment.completed is False


@pytest.mark.django_db
def test_list_payments(api_client, auth_header, test_user):
    # Два платежа вручную
    Payment.objects.create(
        user=test_user,
        stripe_session_id="sess_1",
        amount=5,
        currency="usd",
    )
    Payment.objects.create(
        user=test_user,
        stripe_session_id="sess_2",
        amount=15,
        currency="usd",
    )
    resp = api_client.get("/api/payments/", **auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    ids = {p["id"] for p in data}
    assert ids == set(Payment.objects.values_list('id', flat=True))