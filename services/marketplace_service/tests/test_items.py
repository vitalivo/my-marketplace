import pytest
from django.contrib.gis.geos import Point
from marketplace_app.models import Category, Item


@pytest.mark.django_db
def test_create_item(api_client, auth_header, test_user):
    cat = Category.objects.create(name="Electronics")
    payload = {
        "title": "Smartphone",
        "description": "Test phone",
        "price": "199.99",
        # GeoJSON → будет конвертировано в Point
        "location": {"type": "Point", "coordinates": [30.0, -20.0]},
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

    # Ответ – GeoJSON Feature
    # └─ geometry  – координаты
    # └─ properties – все остальные поля
    assert data["properties"]["title"] == "Smartphone"
    assert data["properties"]["category"] == cat.id
    assert data["properties"]["owner"] == test_user.id
    assert data["geometry"]["type"] == "Point"
    assert data["geometry"]["coordinates"] == [30.0, -20.0]


@pytest.mark.django_db
def test_radius_search(api_client, auth_header, test_user):
    cat = Category.objects.create(name="Books")

    # Товар рядом
    Item.objects.create(
        title="Near book",
        price=10,
        location=Point(30.0, -20.0, srid=4326),
        category=cat,
        owner=test_user,
    )
    # Товар далеко
    Item.objects.create(
        title="Far book",
        price=15,
        location=Point(40.0, -20.0, srid=4326),
        category=cat,
        owner=test_user,
    )

    # Поиск в радиусе 1000 km от (30, -20)
    resp = api_client.get(
        "/api/items/?lat=-20&lon=30&radius=1000",
        **auth_header,
    )
    assert resp.status_code == 200

    # drf‑gis возвращает FeatureCollection:
    # {
    #   "type": "FeatureCollection",
    #   "features": [ {...}, {...} ]
    # }
    collection = resp.json()
    titles = [feat["properties"]["title"] for feat in collection["features"]]
    assert "Near book" in titles
    assert "Far book" not in titles

    # Проверяем, что поле distance сериализовано как число
    for feat in collection["features"]:
        if feat["properties"]["title"] == "Near book":
            dist = feat["properties"]["distance"]
            assert isinstance(dist, (int, float))
            # Должно быть меньше радиуса (1000 km)
            assert 0 <= dist < 1000
            break
    else:
        pytest.fail("Near book не найден в результатах поиска")