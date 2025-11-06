from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: str
    postal_code: str
    country: str = "Germany"
    latitude: float
    longitude: float
    category: str
    image_url: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class Place(PlaceBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
