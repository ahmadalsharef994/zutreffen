"""
Service functions for location-based operations
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from models.place import Place
import math


def get_all_cities(db: Session) -> List[str]:
    """Get list of all unique cities in the database"""
    cities = db.query(distinct(Place.city)).filter(
        Place.is_active == True,
        Place.city.isnot(None)
    ).order_by(Place.city).all()
    return [city[0] for city in cities if city[0]]


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def get_places_near_location(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    limit: int = 100
) -> List[Tuple[Place, float]]:
    """
    Get places near a specific location within a radius
    Returns list of (Place, distance) tuples sorted by distance
    """
    # Get all active places with coordinates
    places = db.query(Place).filter(
        Place.is_active == True,
        Place.latitude.isnot(None),
        Place.longitude.isnot(None)
    ).all()
    
    # Calculate distances and filter by radius
    places_with_distance = []
    for place in places:
        distance = calculate_distance(latitude, longitude, place.latitude, place.longitude)
        if distance <= radius_km:
            places_with_distance.append((place, distance))
    
    # Sort by distance and limit results
    places_with_distance.sort(key=lambda x: x[1])
    return places_with_distance[:limit]


def search_places(
    db: Session,
    query: str,
    city: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100
) -> List[Place]:
    """
    Search places by name, description, address with optional filters
    """
    filters = [Place.is_active == True]
    
    # Text search
    if query:
        search_filter = func.lower(Place.name).contains(query.lower()) | \
                       func.lower(Place.description).contains(query.lower()) | \
                       func.lower(Place.address).contains(query.lower())
        filters.append(search_filter)
    
    # City filter
    if city:
        filters.append(Place.city == city)
    
    # Category filter
    if category:
        filters.append(Place.category == category)
    
    return db.query(Place).filter(*filters).limit(limit).all()
