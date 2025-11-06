import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import engine, Base, SessionLocal
from app.models import User, Place, CheckIn
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

# Import mock data
from mock_data.users import MOCK_USERS
from mock_data.places import MOCK_PLACES
from mock_data.checkins import generate_mock_checkins

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

def seed_users(db: Session):
    """Seed users"""
    print("\n🌱 Seeding users...")
    users = []
    for user_data in MOCK_USERS:
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"],
            hashed_password=get_password_hash(user_data["password"]),
            avatar_url=user_data["avatar_url"],
            bio=user_data["bio"],
            is_active=True
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    print(f"✓ Created {len(users)} users")
    return users

def seed_places(db: Session):
    """Seed places"""
    print("\n🌱 Seeding places...")
    places = []
    for place_data in MOCK_PLACES:
        place = Place(**place_data)
        db.add(place)
        places.append(place)
    
    db.commit()
    print(f"✓ Created {len(places)} places")
    return places

def seed_checkins(db: Session, users, places):
    """Seed checkins"""
    print("\n🌱 Seeding checkins...")
    checkins_data = generate_mock_checkins(users, places)
    checkins = []
    
    for checkin_data in checkins_data:
        checkin = CheckIn(**checkin_data)
        db.add(checkin)
        checkins.append(checkin)
    
    db.commit()
    print(f"✓ Created {len(checkins)} check-ins")
    return checkins

def clear_database(db: Session):
    """Clear all data from database"""
    print("\n🗑️  Clearing database...")
    db.query(CheckIn).delete()
    db.query(Place).delete()
    db.query(User).delete()
    db.commit()
    print("✓ Database cleared")

def main():
    """Main seeding function"""
    print("=" * 50)
    print("🚀 Starting database seeding...")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(db)
        
        # Seed data
        users = seed_users(db)
        places = seed_places(db)
        checkins = seed_checkins(db, users, places)
        
        print("\n" + "=" * 50)
        print("✅ Database seeding completed successfully!")
        print("=" * 50)
        print(f"\n📊 Summary:")
        print(f"   Users: {len(users)}")
        print(f"   Places: {len(places)}")
        print(f"   Check-ins: {len(checkins)}")
        print("\n🔑 Test credentials:")
        print("   Email: max.mueller@example.com")
        print("   Password: password123")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
