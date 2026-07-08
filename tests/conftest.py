import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.database import Base, get_db
from app.main import app
from app.models import Item

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database_file():
    yield
    engine.dispose()


@pytest.fixture(autouse=True)
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def item_payload():
    return {
        "name": "Laptop",
        "description": "Dell laptop",
        "price": 55000,
        "is_active": True,
    }


@pytest.fixture
def create_item(client, item_payload):
    def _create_item(**overrides):
        payload = {**item_payload, **overrides}
        response = client.post("/items", json=payload)
        assert response.status_code == 200
        return response.json()

    return _create_item


@pytest.fixture
def db_item(db_session, item_payload):
    item = Item(**item_payload)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item
