def test_get_item_not_found(client):
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item_not_found(client):
    response = client.put("/items/999", json={"name": "Missing Item"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_item_not_found(client):
    response = client.delete("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
