from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_password_hash
from schemas.user import UserCreate, User, UserUpdate
from db.session import get_db
from models.user import User as UserModel
from core.deps import get_current_active_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all users.
    """
    users = db.query(UserModel).filter(UserModel.is_active == True).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Check if user exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = UserModel(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Update user profile (requires authentication and ownership).
    """
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify ownership
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own profile")
    
    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Handle password separately if provided
    if 'password' in update_data and update_data['password']:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user