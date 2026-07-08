from app.models import Item


def test_create_item_returns_created_data_and_persists_record(client, db_session, item_payload):
    response = client.post("/items", json=item_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_payload["name"]
    assert data["description"] == item_payload["description"]
    assert data["price"] == item_payload["price"]
    assert data["is_active"] is True
    assert "id" in data

    db_item = db_session.get(Item, data["id"])
    assert db_item is not None
    assert db_item.name == item_payload["name"]


def test_get_all_items_returns_persisted_records(client, db_item):
    response = client.get("/items")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0] == {
        "id": db_item.id,
        "name": db_item.name,
        "description": db_item.description,
        "price": db_item.price,
        "is_active": db_item.is_active,
    }


def test_get_item_by_id_returns_expected_record(client, db_item):
    response = client.get(f"/items/{db_item.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": db_item.id,
        "name": db_item.name,
        "description": db_item.description,
        "price": db_item.price,
        "is_active": db_item.is_active,
    }


def test_update_item_returns_updated_data_and_persists_changes(client, db_session, db_item):
    response = client.put(
        f"/items/{db_item.id}",
        json={"name": "Updated Laptop", "price": 60000, "is_active": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_item.id
    assert data["name"] == "Updated Laptop"
    assert data["description"] == db_item.description
    assert data["price"] == 60000
    assert data["is_active"] is False

    db_session.refresh(db_item)
    assert db_item.name == "Updated Laptop"
    assert db_item.price == 60000
    assert db_item.is_active is False


def test_delete_item_removes_record_and_returns_success_message(client, db_session, db_item):
    response = client.delete(f"/items/{db_item.id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

    db_session.expire_all()
    assert db_session.get(Item, db_item.id) is None
    assert client.get(f"/items/{db_item.id}").status_code == 404
