import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {"description": "Missing name", "price": 100},
        {"name": "", "price": 100},
        {"name": "Laptop"},
        {"name": "Laptop", "price": 0},
        {"name": "Laptop", "price": -1},
        {"name": "Laptop", "price": "not-a-number"},
        {"name": "Laptop", "price": 100, "is_active": "not-a-bool"},
        {"name": "Laptop", "price": 100, "unexpected": "field"},
    ],
)
def test_create_item_validation_errors(client, payload):
    response = client.post("/items", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_invalid_json_payload_returns_validation_error(client):
    response = client.post(
        "/items",
        content="{invalid-json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "payload",
    [
        {"name": ""},
        {"price": 0},
        {"price": -1},
        {"price": "not-a-number"},
        {"is_active": "not-a-bool"},
        {"unexpected": "field"},
    ],
)
def test_update_item_validation_errors(client, db_item, payload):
    response = client.put(f"/items/{db_item.id}", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()
