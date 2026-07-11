import os

from app.db_config import build_database_url, read_database_settings

TEST_SETTINGS = read_database_settings("TEST_DB")
for setting_name in ("HOST", "PORT", "NAME", "USER", "PASSWORD"):
    os.environ[f"DB_{setting_name}"] = TEST_SETTINGS[f"TEST_DB_{setting_name}"]

TEST_DATABASE_URL = build_database_url("TEST_DB")
EXPECTED_TEST_DATABASE_NAME = TEST_SETTINGS["TEST_DB_NAME"]

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database import Base, DATABASE_URL, get_db
from app.main import app
from app.models import Item

if DATABASE_URL != TEST_DATABASE_URL:
    raise RuntimeError("Application database URL does not match the configured test database URL.")

engine = create_engine(TEST_DATABASE_URL)
with engine.connect() as connection:
    actual_database_name = connection.execute(text("SELECT current_database()"))
    if actual_database_name.scalar_one() != EXPECTED_TEST_DATABASE_NAME:
        raise RuntimeError("Connected database does not match TEST_DB_NAME.")

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
