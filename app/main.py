from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Item
from .schemas import ItemCreate, ItemOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI SQLAlchemy Docker")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/items", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items", response_model=list[ItemOut])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/sample")
def sample_endpoint():
    return {"message": "This is a sample API endpoint", "status": "success"}
