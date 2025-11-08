from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base

class Place(Base):
    __tablename__ = "places"
    
    # Basic info
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    address = Column(String)
    city = Column(String, index=True)
    postal_code = Column(String, index=True)
    country = Column(String, default="Germany")
    latitude = Column(Float)
    longitude = Column(Float)
    category = Column(String, index=True)  # cafe, restaurant, coworking, etc.
    image_url = Column(String, nullable=True)
    
    # Extended info (from Google Places or OSM)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    opening_hours = Column(JSON, nullable=True)  # Stores array or dict
    rating = Column(Float, nullable=True)
    user_ratings_total = Column(Integer, nullable=True)
    price_level = Column(Integer, nullable=True)  # 0-4 (Google Places)
    business_status = Column(String, nullable=True)  # OPERATIONAL, CLOSED_TEMPORARILY, etc.
    
    # External IDs
    google_place_id = Column(String, nullable=True, index=True)
    osm_id = Column(String, nullable=True, index=True)
    data_source = Column(String, nullable=True)  # 'google_places', 'openstreetmap', 'manual'
    
    # System fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    checkins = relationship("CheckIn", back_populates="place")
