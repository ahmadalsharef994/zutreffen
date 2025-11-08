"""
Import scraped JSON data to Zutreffen database

This script imports places from JSON files into your Zutreffen app database.

Usage:
    python3 import_to_db.py

Options:
    - Import all places
    - Import specific city
    - Import specific category
    - Skip duplicates automatically
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from sqlalchemy.orm import Session
    from models.place import Place
    from db.session import SessionLocal, engine, Base
except ImportError:
    print("❌ Error: Cannot import Zutreffen modules")
    print("Make sure you're running this from the project root")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseImporter:
    """Import JSON data to Zutreffen database."""
    
    def __init__(self):
        self.json_dir = Path(__file__).parent / 'data' / 'json_output'
        self.db: Session = SessionLocal()
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
    
    def load_json(self, filename: str = 'all_places.json') -> List[Dict]:
        """Load places from JSON file."""
        json_file = self.json_dir / filename
        
        if not json_file.exists():
            logger.error(f"JSON file not found: {json_file}")
            logger.info("Run scrape.py first to generate data")
            return []
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both list and dict formats
        if isinstance(data, dict):
            # If it's places_by_city.json or similar
            places = []
            for city_places in data.values():
                places.extend(city_places)
            return places
        else:
            return data
    
    def import_places(
        self, 
        places: List[Dict],
        city_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        skip_duplicates: bool = True
    ) -> int:
        """Import places to database."""
        imported = 0
        skipped = 0
        
        logger.info(f"Starting import of {len(places)} places...")
        
        for i, place_data in enumerate(places):
            try:
                # Apply filters
                if city_filter and place_data['city'] != city_filter:
                    continue
                if category_filter and place_data['category'] != category_filter:
                    continue
                
                # Check for duplicates
                if skip_duplicates:
                    existing = self.db.query(Place).filter(
                        Place.name == place_data['name'],
                        Place.latitude == place_data['latitude'],
                        Place.longitude == place_data['longitude']
                    ).first()
                    
                    if existing:
                        skipped += 1
                        continue
                
                # Create place
                new_place = Place(
                    name=place_data['name'],
                    description=place_data.get('description', ''),
                    address=place_data.get('address', ''),
                    city=place_data['city'],
                    postal_code=place_data.get('postal_code', ''),
                    country="Germany",
                    latitude=float(place_data['latitude']),
                    longitude=float(place_data['longitude']),
                    category=place_data['category'],
                    image_url=place_data.get('image_url'),
                    phone=place_data.get('phone'),
                    website=place_data.get('website'),
                    opening_hours=place_data.get('opening_hours'),
                    rating=place_data.get('rating'),
                    user_ratings_total=place_data.get('user_ratings_total'),
                    price_level=place_data.get('price_level'),
                    business_status=place_data.get('business_status', 'OPERATIONAL'),
                    google_place_id=place_data.get('google_place_id'),
                    osm_id=place_data.get('osm_id'),
                    data_source=place_data.get('data_source', 'scraped'),
                    is_active=True
                )
                
                self.db.add(new_place)
                imported += 1
                
                # Commit in batches
                if imported % 500 == 0:
                    self.db.commit()
                    logger.info(f"Progress: {imported} imported, {skipped} skipped")
            
            except Exception as e:
                logger.error(f"Error importing place {place_data.get('name')}: {e}")
                continue
        
        # Final commit
        self.db.commit()
        
        logger.info(f"\n✅ Import complete!")
        logger.info(f"   Imported: {imported}")
        logger.info(f"   Skipped: {skipped}")
        logger.info(f"   Total in DB: {self.db.query(Place).count()}")
        
        return imported
    
    def show_stats(self):
        """Show database statistics."""
        total = self.db.query(Place).count()
        
        if total == 0:
            print("\n📊 Database is empty")
            return
        
        print("\n📊 Database Statistics:")
        print(f"   Total places: {total}")
        
        # By city
        print("\n   Top 10 cities:")
        from sqlalchemy import func
        cities = self.db.query(
            Place.city,
            func.count(Place.id).label('count')
        ).group_by(Place.city).order_by(func.count(Place.id).desc()).limit(10).all()
        
        for city, count in cities:
            print(f"      {city}: {count}")
        
        # By category
        print("\n   By category:")
        categories = self.db.query(
            Place.category,
            func.count(Place.id).label('count')
        ).group_by(Place.category).order_by(func.count(Place.id).desc()).all()
        
        for category, count in categories:
            print(f"      {category}: {count}")
    
    def clear_all(self):
        """Clear all places from database."""
        count = self.db.query(Place).count()
        
        if count == 0:
            print("Database is already empty")
            return
        
        confirm = input(f"\n⚠️  Delete all {count} places? (type 'DELETE' to confirm): ")
        if confirm == 'DELETE':
            self.db.query(Place).delete()
            self.db.commit()
            logger.info(f"✅ Deleted {count} places")
        else:
            print("Cancelled")
    
    def close(self):
        """Close database connection."""
        self.db.close()


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("📥 IMPORT JSON TO DATABASE")
    print("="*60)
    
    importer = DatabaseImporter()
    
    # Check if JSON data exists
    json_file = importer.json_dir / 'all_places.json'
    if not json_file.exists():
        print(f"\n❌ No JSON data found at: {json_file}")
        print("\n🚀 Run this first:")
        print("   python3 scrape.py")
        return
    
    # Show current database stats
    importer.show_stats()
    
    # Menu
    print("\n📋 Options:")
    print("   1. Import all places")
    print("   2. Import specific city")
    print("   3. Import specific category")
    print("   4. Show database stats")
    print("   5. Clear all data")
    print("   0. Exit")
    
    choice = input("\nChoice (0-5): ")
    
    if choice == '1':
        places = importer.load_json('all_places.json')
        if places:
            proceed = input(f"\nImport {len(places)} places? (y/N): ")
            if proceed.lower() == 'y':
                importer.import_places(places)
    
    elif choice == '2':
        # Load metadata to show available cities
        metadata_file = importer.json_dir / 'metadata.json'
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            print("\nAvailable cities:")
            for city, count in sorted(metadata['places_by_city'].items())[:20]:
                print(f"   {city} ({count} places)")
            print("   ... and more")
        
        city = input("\nEnter city name: ")
        places = importer.load_json('all_places.json')
        if places:
            importer.import_places(places, city_filter=city)
    
    elif choice == '3':
        # Show categories
        print("\nCategories:")
        categories = ['cafe', 'restaurant', 'bar', 'library', 'hotel_lobby', 
                     'coworking', 'gym_cafe', 'cinema_lobby']
        for cat in categories:
            print(f"   {cat}")
        
        category = input("\nEnter category: ")
        places = importer.load_json('all_places.json')
        if places:
            importer.import_places(places, category_filter=category)
    
    elif choice == '4':
        importer.show_stats()
    
    elif choice == '5':
        importer.clear_all()
    
    else:
        print("👋 Goodbye!")
    
    importer.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
