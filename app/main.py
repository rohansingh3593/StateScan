from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Item
from .schemas import ItemCreate, ItemResponse, ItemUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI SQLAlchemy Docker")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    for field, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}


@app.get("/sample")
def sample_endpoint():
    return {"message": "This is a sample API endpoint", "status": "success"}
