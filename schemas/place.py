from pydantic import BaseModel
from typing import Optional, List, Union
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
    
    # Extended fields
    phone: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[Union[List[str], dict]] = None
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    price_level: Optional[int] = None
    business_status: Optional[str] = None
    google_place_id: Optional[str] = None
    osm_id: Optional[str] = None
    data_source: Optional[str] = None

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
    phone: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[Union[List[str], dict]] = None
    rating: Optional[float] = None
    price_level: Optional[int] = None
    business_status: Optional[str] = None
    is_active: Optional[bool] = None

class Place(PlaceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
