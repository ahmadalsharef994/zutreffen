from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    languages: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    why_here: Optional[str] = None

class User(UserBase):
    id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    languages: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    why_here: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True