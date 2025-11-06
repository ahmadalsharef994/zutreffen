# Mock Data

This directory contains mock data and seeding scripts for the Zutreffen application.

## Contents

- `users.py` - 10 realistic German user profiles with avatars
- `places.py` - 20 real places across major German cities (Berlin, Munich, Hamburg, Frankfurt, Cologne, Stuttgart, Düsseldorf)
- `checkins.py` - Generator for realistic check-in data
- `seed_database.py` - Main script to populate the database

## Real Coordinates

All places use real coordinates from German cities:
- **Berlin**: Cafés, coworking spaces, and parks
- **Munich**: Popular meeting spots
- **Hamburg**: Harbor area locations
- **Frankfurt**: City center venues
- **Cologne**: Rhine-side places
- **Stuttgart**: Central locations
- **Düsseldorf**: Trendy neighborhoods

## Running the Seed Script

```bash
# From the project root directory
python mock_data/seed_database.py
```

This will:
1. Create all database tables
2. Clear existing data
3. Seed 10 users
4. Seed 20 places
5. Generate ~30 check-ins

## Test Credentials

After seeding, you can log in with:
- **Email**: max.mueller@example.com
- **Password**: password123

Or any other user email with `password123`.

## Images

- User avatars: Using pravatar.cc for realistic profile pictures
- Place images: Using Unsplash for high-quality venue photos

## Data Structure

### Users
- Realistic German names
- Professional bios
- Avatar images
- Various professions (developer, designer, student, etc.)

### Places
- Real addresses and postal codes
- Accurate GPS coordinates
- Categories: cafe, coworking, park, restaurant
- Professional descriptions
- High-quality images

### Check-ins
- Random distribution across users and places
- Realistic timestamps (past 7 days)
- 70% active, 30% ended
- Optional messages
- Realistic durations (1-4 hours)
