from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CheckInBase(BaseModel):
    place_id: int
    message: Optional[str] = None
    duration_hours: Optional[int] = 2  # Default 2 hours

class CheckInCreate(CheckInBase):
    pass

class CheckInUpdate(BaseModel):
    message: Optional[str] = None
    status: Optional[str] = None

class CheckIn(CheckInBase):
    id: int
    user_id: int
    status: str
    duration_hours: int
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True
