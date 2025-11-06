from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    address = Column(String)
    city = Column(String, index=True)
    postal_code = Column(String, index=True)
    country = Column(String, default="Germany")
    latitude = Column(Float)
    longitude = Column(Float)
    category = Column(String, index=True)  # cafe, restaurant, park, coworking, etc.
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    checkins = relationship("CheckIn", back_populates="place")
