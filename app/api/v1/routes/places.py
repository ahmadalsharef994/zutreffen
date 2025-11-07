from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.place import Place
from app.models.user import User
from app.schemas.place import Place as PlaceSchema, PlaceCreate, PlaceUpdate
from app.api.deps import get_current_active_user



const categories = [
    // Food & Drink
    'cafe', 'bar', 'restaurant', 'fast_food', 'kiosk',
    
    // Hospitality
    'hotel_lobby', 'hostel', 'airport_lounge',
    
    // Work & Study
    'coworking', 'library', 'business_center', 'university_cafe',
    
    // Shopping & Entertainment
    'mall_food_court', 'cinema_lobby', 'gaming_cafe', 'entertainment_venue',
    
    // Transportation
    'train_station_cafe', 'bus_terminal', 'service_station',
    
    // Fitness & Wellness
    'gym_cafe', 'spa_lounge'
];

router = APIRouter()

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