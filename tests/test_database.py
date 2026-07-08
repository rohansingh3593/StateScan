from sqlalchemy import text

from app.models import Item


def test_database_connection(db_session):
    assert db_session.execute(text("SELECT 1")).scalar_one() == 1


def test_database_create_read_update_delete(db_session, item_payload):
    item = Item(**item_payload)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    persisted_item = db_session.get(Item, item.id)
    assert persisted_item is not None
    assert persisted_item.name == item_payload["name"]

    persisted_item.name = "Updated Laptop"
    persisted_item.price = 60000
    db_session.commit()
    db_session.refresh(persisted_item)

    updated_item = db_session.get(Item, item.id)
    assert updated_item.name == "Updated Laptop"
    assert updated_item.price == 60000

    db_session.delete(updated_item)
    db_session.commit()

    assert db_session.get(Item, item.id) is None
