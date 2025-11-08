from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from db.session import get_db
from models.place import Place
from models.user import User
from schemas.place import Place as PlaceSchema, PlaceCreate, PlaceUpdate
from core.deps import get_current_active_user
from services.location import get_all_cities, get_places_near_location, search_places


router = APIRouter()


class PlaceWithDistance(BaseModel):
    place: PlaceSchema
    distance_km: float
    
    class Config:
        orm_mode = True

@router.get("/", response_model=List[PlaceSchema])
async def list_places(
    skip: int = 0,
    limit: int = 100,
    city: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    List all places with optional filters.
    """
    query = db.query(Place).filter(Place.is_active == True)
    
    if city:
        query = query.filter(Place.city == city)
    if category:
        query = query.filter(Place.category == category)
    
    places = query.offset(skip).limit(limit).all()
    return places

@router.get("/{place_id}", response_model=PlaceSchema)
async def get_place(place_id: int, db: Session = Depends(get_db)):
    """
    Get a specific place by ID.
    """
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place

@router.post("/", response_model=PlaceSchema, status_code=status.HTTP_201_CREATED)
async def create_place(
    place_data: PlaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new place (requires authentication).
    """
    new_place = Place(**place_data.dict())
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

@router.put("/{place_id}", response_model=PlaceSchema)
async def update_place(
    place_id: int,
    place_data: PlaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a place (requires authentication).
    """
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Update only provided fields
    update_data = place_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(place, field, value)
    
    db.commit()
    db.refresh(place)
    return place

@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place(
    place_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a place (soft delete - sets is_active to False).
    """
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    place.is_active = False
    db.commit()
    return None


@router.get("/cities/all", response_model=List[str])
async def get_cities(db: Session = Depends(get_db)):
    """
    Get list of all unique cities in the database.
    """
    cities = get_all_cities(db)
    return cities


@router.get("/search/text", response_model=List[PlaceSchema])
async def search_places_endpoint(
    q: Optional[str] = Query(None, description="Search query"),
    city: Optional[str] = Query(None, description="Filter by city"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, le=500, description="Max results"),
    db: Session = Depends(get_db)
):
    """
    Search places by text query with optional filters.
    """
    places = search_places(db, query=q, city=city, category=category, limit=limit)
    return places


@router.get("/nearby/gps", response_model=List[PlaceWithDistance])
async def get_nearby_places(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: float = Query(10.0, ge=0.1, le=50, description="Search radius in km"),
    limit: int = Query(100, le=500, description="Max results"),
    db: Session = Depends(get_db)
):
    """
    Get places near a GPS location within a radius.
    Returns places sorted by distance.
    """
    places_with_distance = get_places_near_location(
        db, latitude=lat, longitude=lng, radius_km=radius, limit=limit
    )
    
    result = []
    for place, distance in places_with_distance:
        result.append({
            "place": PlaceSchema.from_orm(place),
            "distance_km": round(distance, 2)
        })
    
    return result