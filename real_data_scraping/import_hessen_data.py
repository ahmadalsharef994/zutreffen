"""
Import Hessen places from scraped data + create mock users and checkins
Combines real place data with mock social data
"""
import json
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal
from models.user import User
from models.place import Place
from models.checkin import CheckIn
from core.security import get_password_hash

def import_hessen_data():
    db = SessionLocal()
    
    try:
        print("🔍 Loading scraped places data...")
        with open('real_data_scraping/data/json_output/all_places.json', 'r') as f:
            all_places = json.load(f)
        
        print(f"📊 Total places in file: {len(all_places):,}")
        
        # Filter Hessen cities
        hessen_keywords = [
            'Frankfurt', 'Darmstadt', 'Wiesbaden', 'Marburg', 'Offenbach', 
            'Kassel', 'Gießen', 'Fulda', 'Hanau', 'Rüsselsheim'
        ]
        
        hessen_places = [
            p for p in all_places 
            if any(kw.lower() in p.get('city', '').lower() for kw in hessen_keywords)
        ]
        
        print(f"🎯 Hessen places found: {len(hessen_places):,}")
        
        # Limit to reasonable number for prototype (500 places)
        hessen_places = hessen_places[:500]
        
        print(f"📥 Importing {len(hessen_places)} places to database...")
        
        # Import places
        imported_places = []
        for place_data in hessen_places:
            try:
                place = Place(
                    name=place_data.get('name'),
                    address=place_data.get('address', ''),
                    city=place_data.get('city', ''),
                    postal_code=place_data.get('postal_code'),
                    country='Germany',
                    latitude=place_data.get('latitude'),
                    longitude=place_data.get('longitude'),
                    category=place_data.get('category', 'other'),
                    description=place_data.get('description'),
                    phone=place_data.get('phone'),
                    website=place_data.get('website'),
                    opening_hours=place_data.get('opening_hours'),
                    rating=place_data.get('rating'),
                    user_ratings_total=place_data.get('user_ratings_total'),
                    price_level=place_data.get('price_level'),
                    business_status=place_data.get('business_status'),
                    google_place_id=place_data.get('google_place_id'),
                    data_source=place_data.get('data_source', 'google'),
                    is_active=True
                )
                db.add(place)
                imported_places.append(place)
            except Exception as e:
                print(f"⚠️  Error importing place {place_data.get('name')}: {e}")
        
        db.commit()
        print(f"✅ Imported {len(imported_places)} places")
        
        # Count by city
        from collections import Counter
        city_counts = Counter([p.city for p in imported_places])
        print("\n📍 Places by city:")
        for city, count in sorted(city_counts.items(), key=lambda x: -x[1]):
            print(f"   {city}: {count} places")
        
        # Create mock users
        print("\n👥 Creating mock users...")
        users_data = [
            {
                "email": "test@test.com",
                "username": "test_user",
                "full_name": "Test User",
                "bio": "Just testing the app",
                "languages": ["English", "German"],
                "interests": ["Tech", "Coffee"],
                "why_here": "Living"
            },
            {
                "email": "sarah.mueller@email.com",
                "username": "sarah_m",
                "full_name": "Sarah Müller",
                "bio": "Software engineer, love coffee and books",
                "languages": ["German", "English"],
                "interests": ["Tech", "Coffee", "Reading", "Hiking"],
                "why_here": "Living"
            },
            {
                "email": "ahmad.ali@email.com",
                "username": "ahmad_a",
                "full_name": "Ahmad Ali",
                "bio": "Designer from Syria, exploring Germany",
                "languages": ["Arabic", "English", "German"],
                "interests": ["Design", "Photography", "Travel", "Food"],
                "why_here": "Traveling"
            },
            {
                "email": "maria.garcia@email.com",
                "username": "maria_g",
                "full_name": "Maria Garcia",
                "bio": "Spanish teacher, music lover",
                "languages": ["Spanish", "English", "German"],
                "interests": ["Music", "Teaching", "Dancing", "Languages"],
                "why_here": "Living"
            },
            {
                "email": "john.smith@email.com",
                "username": "john_s",
                "full_name": "John Smith",
                "bio": "American expat, tech startup founder",
                "languages": ["English", "German"],
                "interests": ["Tech", "Startups", "Running", "Networking"],
                "why_here": "Living"
            },
            {
                "email": "yuki.tanaka@email.com",
                "username": "yuki_t",
                "full_name": "Yuki Tanaka",
                "bio": "Japanese exchange student",
                "languages": ["Japanese", "English"],
                "interests": ["Anime", "Gaming", "Cooking", "Culture"],
                "why_here": "Studying"
            },
            {
                "email": "lisa.schmidt@email.com",
                "username": "lisa_s",
                "full_name": "Lisa Schmidt",
                "bio": "Freelance writer and coffee addict",
                "languages": ["German", "English", "French"],
                "interests": ["Writing", "Coffee", "Art", "Museums"],
                "why_here": "Living"
            },
            {
                "email": "david.brown@email.com",
                "username": "david_b",
                "full_name": "David Brown",
                "bio": "Digital nomad, remote worker",
                "languages": ["English"],
                "interests": ["Remote Work", "Travel", "Tech", "Fitness"],
                "why_here": "Traveling"
            },
            {
                "email": "emma.johnson@email.com",
                "username": "emma_j",
                "full_name": "Emma Johnson",
                "bio": "Graphic designer, art enthusiast",
                "languages": ["English", "German"],
                "interests": ["Design", "Art", "Photography", "Cycling"],
                "why_here": "Living"
            },
            {
                "email": "mohamed.hassan@email.com",
                "username": "mohamed_h",
                "full_name": "Mohamed Hassan",
                "bio": "Engineering student from Egypt",
                "languages": ["Arabic", "English", "German"],
                "interests": ["Engineering", "Soccer", "Cooking", "Travel"],
                "why_here": "Studying"
            }
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                bio=user_data["bio"],
                languages=user_data["languages"],
                interests=user_data["interests"],
                why_here=user_data["why_here"],
                hashed_password=get_password_hash("test"),
                is_active=True
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"✅ Created {len(users)} mock users")
        
        # Create mock checkins
        print("\n📍 Creating mock check-ins...")
        checkin_messages = [
            "Working on my laptop for a few hours ☕",
            "Meeting new people, come say hi! 👋",
            "Having coffee and reading 📚",
            "Working remotely today 💻",
            "Enjoying the atmosphere ☀️",
            "Looking to practice German 🇩🇪",
            "Anyone want to grab lunch? 🍽️",
            "Study session 📖",
            "Just chilling for a bit ☕",
            "Open to chat about tech/startups 💡"
        ]
        
        now = datetime.utcnow()
        checkins = []
        
        # Create 25 active checkins
        for i in range(25):
            user = random.choice(users)
            place = random.choice(imported_places[:100])  # From first 100 places
            duration = random.choice([1, 2, 3, 4, 5, 6, 8, 10])
            checkin_time = now - timedelta(minutes=random.randint(10, 180))
            
            checkin = CheckIn(
                user_id=user.id,
                place_id=place.id,
                message=random.choice(checkin_messages),
                duration_hours=duration,
                check_in_time=checkin_time,
                status="active"
            )
            db.add(checkin)
            checkins.append(checkin)
        
        db.commit()
        print(f"✅ Created {len(checkins)} mock check-ins")
        
        print("\n🎉 Import complete!")
        print(f"   📍 {len(imported_places)} places")
        print(f"   👥 {len(users)} users")
        print(f"   ✅ {len(checkins)} active check-ins")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting Hessen data import...")
    print("⚠️  This will clear the database and import fresh data\n")
    
    # Recreate database
    print("🗑️  Recreating database...")
    from db.session import engine, Base
    from models.user import User
    from models.place import Place
    from models.checkin import CheckIn
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database recreated\n")
    
    import_hessen_data()
