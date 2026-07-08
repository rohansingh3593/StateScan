from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    is_active: bool = True


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class ItemResponse(ItemCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
