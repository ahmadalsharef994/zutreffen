from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from db.session import get_db
from models.checkin import CheckIn
from models.place import Place
from models.user import User
from schemas.checkin import CheckIn as CheckInSchema, CheckInCreate, CheckInUpdate
from core.deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[CheckInSchema])
async def list_checkins(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all checkins. By default shows only active check-ins.
    """
    query = db.query(CheckIn)
    
    if active_only:
        query = query.filter(CheckIn.status == "active")
    
    checkins = query.order_by(CheckIn.check_in_time.desc()).offset(skip).limit(limit).all()
    return checkins

@router.get("/my", response_model=List[CheckInSchema])
async def my_checkins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's check-ins.
    """
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id
    ).order_by(CheckIn.check_in_time.desc()).offset(skip).limit(limit).all()
    return checkins

@router.get("/{checkin_id}", response_model=CheckInSchema)
async def get_checkin(checkin_id: int, db: Session = Depends(get_db)):
    """
    Get a specific check-in by ID.
    """
    checkin = db.query(CheckIn).filter(CheckIn.id == checkin_id).first()
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return checkin

@router.post("/", response_model=CheckInSchema, status_code=status.HTTP_201_CREATED)
async def create_checkin(
    checkin_data: CheckInCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new check-in (requires authentication).
    """
    # Verify place exists
    place = db.query(Place).filter(Place.id == checkin_data.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Check if user already has an active checkin
    active_checkin = db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id,
        CheckIn.status == "active"
    ).first()
    
    if active_checkin:
        raise HTTPException(
            status_code=400,
            detail="You already have an active check-in. Please end it first."
        )
    
    # Create new check-in
    new_checkin = CheckIn(
        user_id=current_user.id,
        place_id=checkin_data.place_id,
        message=checkin_data.message,
        status="active"
    )
    
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)
    return new_checkin

@router.post("/{checkin_id}/end", response_model=CheckInSchema)
async def end_checkin(
    checkin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    End a check-in (requires authentication and ownership).
    """
    checkin = db.query(CheckIn).filter(CheckIn.id == checkin_id).first()
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    
    # Verify ownership
    if checkin.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only end your own check-ins"
        )
    
    if checkin.status == "ended":
        raise HTTPException(status_code=400, detail="Check-in already ended")
    
    checkin.status = "ended"
    checkin.check_out_time = datetime.utcnow()
    
    db.commit()
    db.refresh(checkin)
    return checkin

@router.delete("/{checkin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checkin(
    checkin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a check-in (requires authentication and ownership).
    """
    checkin = db.query(CheckIn).filter(CheckIn.id == checkin_id).first()
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    
    # Verify ownership
    if checkin.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own check-ins"
        )
    
    db.delete(checkin)
    db.commit()
    return None