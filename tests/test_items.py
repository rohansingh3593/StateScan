import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_item():
    response = client.post(
        "/items",
        json={
            "name": "Laptop",
            "description": "Dell laptop",
            "price": 55000,
            "is_active": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 55000
    assert data["is_active"] is True
    assert "id" in data


def test_get_all_items():
    client.post(
        "/items",
        json={
            "name": "Mouse",
            "description": "Wireless mouse",
            "price": 1200,
            "is_active": True,
        },
    )

    response = client.get("/items")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mouse"


def test_get_item_by_id():
    create_response = client.post(
        "/items",
        json={
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": 3000,
            "is_active": True,
        },
    )

    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Keyboard"


def test_update_item():
    create_response = client.post(
        "/items",
        json={
            "name": "Old Laptop",
            "description": "Old description",
            "price": 40000,
            "is_active": True,
        },
    )

    item_id = create_response.json()["id"]

    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "Updated Laptop",
            "price": 60000,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Laptop"
    assert data["price"] == 60000


def test_delete_item():
    create_response = client.post(
        "/items",
        json={
            "name": "Phone",
            "description": "Android phone",
            "price": 25000,
            "is_active": True,
        },
    )

    item_id = create_response.json()["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"


def test_get_item_not_found():
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_create_item_validation_error():
    response = client.post(
        "/items",
        json={
            "name": "",
            "price": 0,
        },
    )

    assert response.status_code == 422
