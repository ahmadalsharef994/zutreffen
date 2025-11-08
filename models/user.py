from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    
    # New fields for social matching
    languages = Column(JSON, nullable=True)  # ["German", "English", "Arabic"]
    interests = Column(JSON, nullable=True)  # ["Tech", "Coffee", "Travel"]
    why_here = Column(String, nullable=True)  # "Traveling", "Living", "Visiting"
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    checkins = relationship("CheckIn", back_populates="user")