import pytest
from django.contrib.gis.geos import Point
from marketplace_app.models import Category, Item

@pytest.mark.django_db
def test_create_item(api_client, auth_header):
    cat = Category.objects.create(name='Electronics')
    payload = {
        "title": "Smartphone",
        "description": "Test phone",
        "price": "199.99",
        "location": {"type": "Point", "coordinates": [30.0, -20.0]},  # lon, lat
        "category": cat.id,
    }
    resp = api_client.post(
        "/api/items/",
        payload,
        format="json",
        **auth_header,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Smartphone"
    assert data["category"] == cat.id


@pytest.mark.django_db
def test_radius_search(api_client, auth_header):
    cat = Category.objects.create(name="Books")
    # Товар рядом
    Item.objects.create(
        title="Near book",
        price=10,
        location=Point(30.0, -20.0, srid=4326),
        category=cat,
        owner=auth_header["user"],          # <-- реальный объект User
    )
    # Товар далеко
    Item.objects.create(
        title="Far book",
        price=15,
        location=Point(40.0, -20.0, srid=4326),
        category=cat,
        owner=auth_header["user"],
    )

    # Поиск в радиусе 1000 km (≈9° долготы)
    resp = api_client.get(
        "/api/items/?lat=-20&lon=30&radius=1000",
        **auth_header,
    )
    assert resp.status_code == 200
    titles = [i["title"] for i in resp.json()]
    assert "Near book" in titles
    assert "Far book" not in titles