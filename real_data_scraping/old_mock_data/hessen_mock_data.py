"""
Mock data focused on Hessen region with time-based checkins
"""
from datetime import datetime, timedelta
from db.session import SessionLocal
from models.user import User
from models.place import Place
from models.checkin import CheckIn
from core.security import get_password_hash
import random

def create_hessen_mock_data():
    db = SessionLocal()
    
    try:
        # Create mock users with profiles
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
        
        # Create ~50 places in Hessen (Frankfurt, Darmstadt, Wiesbaden, Offenbach, Marburg)
        places_data = [
            # Frankfurt (20 places)
            {"name": "Café Hauptwache", "city": "Frankfurt am Main", "address": "An der Hauptwache 15", "lat": 50.1136, "lng": 8.6797, "category": "cafe", "desc": "Historic café in the heart of Frankfurt"},
            {"name": "Kleinmarkthalle", "city": "Frankfurt am Main", "address": "Hasengasse 5-7", "lat": 50.1119, "lng": 8.6832, "category": "market", "desc": "Traditional market hall with local food"},
            {"name": "MainCafé", "city": "Frankfurt am Main", "address": "Schaumainkai 17", "lat": 50.1067, "lng": 8.6772, "category": "cafe", "desc": "Riverside café with beautiful views"},
            {"name": "Coworking Frankfurt", "city": "Frankfurt am Main", "address": "Mainzer Landstraße 41", "lat": 50.1083, "lng": 8.6647, "category": "coworking", "desc": "Modern coworking space"},
            {"name": "Palmengarten", "city": "Frankfurt am Main", "address": "Siesmayerstraße 61", "lat": 50.1225, "lng": 8.6570, "category": "park", "desc": "Beautiful botanical garden"},
            {"name": "Frankfurter Bücherei", "city": "Frankfurt am Main", "address": "Zeil 126", "lat": 50.1147, "lng": 8.6897, "category": "library", "desc": "Public library and study space"},
            {"name": "Römerberg Square", "city": "Frankfurt am Main", "address": "Römerberg 26", "lat": 50.1103, "lng": 8.6820, "category": "landmark", "desc": "Historic town square"},
            {"name": "Espresso Bar Frankfurt", "city": "Frankfurt am Main", "address": "Bockenheimer Landstraße 21", "lat": 50.1167, "lng": 8.6658, "category": "cafe", "desc": "Specialty coffee bar"},
            {"name": "Goethe University Library", "city": "Frankfurt am Main", "address": "Campus Westend", "lat": 50.1278, "lng": 8.6700, "category": "library", "desc": "University library open to public"},
            {"name": "Sachsenhausen", "city": "Frankfurt am Main", "address": "Alt-Sachsenhausen 23", "lat": 50.1040, "lng": 8.6770, "category": "bar", "desc": "Traditional apple wine district"},
            {"name": "Café Karin", "city": "Frankfurt am Main", "address": "Großer Hirschgraben 28", "lat": 50.1125, "lng": 8.6815, "category": "cafe", "desc": "Cozy café near Goethe House"},
            {"name": "MyZeil Shopping", "city": "Frankfurt am Main", "address": "Zeil 106", "lat": 50.1152, "lng": 8.6870, "category": "shopping", "desc": "Modern shopping center"},
            {"name": "Berger Straße Café", "city": "Frankfurt am Main", "address": "Berger Straße 142", "lat": 50.1236, "lng": 8.7011, "category": "cafe", "desc": "Local neighborhood café"},
            {"name": "Eiserner Steg", "city": "Frankfurt am Main", "address": "Eiserner Steg", "lat": 50.1083, "lng": 8.6817, "category": "landmark", "desc": "Famous pedestrian bridge"},
            {"name": "Konstablerwache Café", "city": "Frankfurt am Main", "address": "Konstabler Wache", "lat": 50.1150, "lng": 8.6925, "category": "cafe", "desc": "Busy café at transport hub"},
            {"name": "Senckenberg Museum", "city": "Frankfurt am Main", "address": "Senckenberganlage 25", "lat": 50.1172, "lng": 8.6500, "category": "museum", "desc": "Natural history museum"},
            {"name": "Nordend Café", "city": "Frankfurt am Main", "address": "Oeder Weg 34", "lat": 50.1236, "lng": 8.6892, "category": "cafe", "desc": "Hip café in Nordend district"},
            {"name": "Frankfurt Book Fair", "city": "Frankfurt am Main", "address": "Ludwig-Erhard-Anlage 1", "lat": 50.1117, "lng": 8.6436, "category": "venue", "desc": "International book fair venue"},
            {"name": "Opernplatz", "city": "Frankfurt am Main", "address": "Opernplatz", "lat": 50.1156, "lng": 8.6722, "category": "landmark", "desc": "Opera house square"},
            {"name": "Westend Campus Café", "city": "Frankfurt am Main", "address": "Grüneburgplatz 1", "lat": 50.1267, "lng": 8.6644, "category": "cafe", "desc": "Student café on campus"},
            
            # Darmstadt (10 places)
            {"name": "Café Chaos", "city": "Darmstadt", "address": "Wilhelminenstraße 15", "lat": 49.8728, "lng": 8.6511, "category": "cafe", "desc": "Alternative café and cultural center"},
            {"name": "Mathildenhöhe", "city": "Darmstadt", "address": "Olbrichweg 13A", "lat": 49.8761, "lng": 8.6706, "category": "landmark", "desc": "Art nouveau colony"},
            {"name": "TU Darmstadt Library", "city": "Darmstadt", "address": "Dolivostraße 15", "lat": 49.8775, "lng": 8.6544, "category": "library", "desc": "University library"},
            {"name": "Herrngarten Park", "city": "Darmstadt", "address": "Herrngarten", "lat": 49.8783, "lng": 8.6589, "category": "park", "desc": "Large public park"},
            {"name": "Luisenplatz", "city": "Darmstadt", "address": "Luisenplatz", "lat": 49.8719, "lng": 8.6497, "category": "landmark", "desc": "Central square with monument"},
            {"name": "Café Schöne Aussicht", "city": "Darmstadt", "address": "Landgraf-Georg-Straße 19", "lat": 49.8692, "lng": 8.6528, "category": "cafe", "desc": "Café with nice views"},
            {"name": "Centralstation", "city": "Darmstadt", "address": "Im Carree", "lat": 49.8722, "lng": 8.6303, "category": "club", "desc": "Popular nightclub and event venue"},
            {"name": "Marktplatz Darmstadt", "city": "Darmstadt", "address": "Marktplatz", "lat": 49.8725, "lng": 8.6508, "category": "market", "desc": "Weekly market square"},
            {"name": "Café Extrablatt", "city": "Darmstadt", "address": "Rheinstraße 26", "lat": 49.8715, "lng": 8.6489, "category": "cafe", "desc": "Chain café with outdoor seating"},
            {"name": "Vivarium Darmstadt", "city": "Darmstadt", "address": "Schnampelweg 5", "lat": 49.8839, "lng": 8.6842, "category": "zoo", "desc": "Small zoo and park"},
            
            # Wiesbaden (10 places)
            {"name": "Café Klatsch", "city": "Wiesbaden", "address": "Wilhelmstraße 36", "lat": 50.0825, "lng": 8.2400, "category": "cafe", "desc": "Traditional café"},
            {"name": "Kurhaus Wiesbaden", "city": "Wiesbaden", "address": "Kurhausplatz 1", "lat": 50.0867, "lng": 8.2453, "category": "landmark", "desc": "Historic spa building"},
            {"name": "Neroberg", "city": "Wiesbaden", "address": "Neroberg", "lat": 50.0958, "lng": 8.2344, "category": "park", "desc": "Hill with panoramic views"},
            {"name": "Marktplatz Wiesbaden", "city": "Wiesbaden", "address": "Marktplatz", "lat": 50.0817, "lng": 8.2428, "category": "market", "desc": "City market square"},
            {"name": "Café Maldaner", "city": "Wiesbaden", "address": "Marktstraße 34", "lat": 50.0822, "lng": 8.2422, "category": "cafe", "desc": "Historic café and restaurant"},
            {"name": "Stadtbibliothek Wiesbaden", "city": "Wiesbaden", "address": "Hochstättenstraße 6-10", "lat": 50.0794, "lng": 8.2400, "category": "library", "desc": "City library"},
            {"name": "Warmer Damm Park", "city": "Wiesbaden", "address": "Warmer Damm", "lat": 50.0886, "lng": 8.2508, "category": "park", "desc": "Park near Kurhaus"},
            {"name": "Café Maingold", "city": "Wiesbaden", "address": "Rheingaustraße 22", "lat": 50.0811, "lng": 8.2350, "category": "cafe", "desc": "Modern café"},
            {"name": "Museum Wiesbaden", "city": "Wiesbaden", "address": "Friedrich-Ebert-Allee 2", "lat": 50.0853, "lng": 8.2428, "category": "museum", "desc": "Art and nature museum"},
            {"name": "Coworking Wiesbaden", "city": "Wiesbaden", "address": "Bahnhofstraße 10", "lat": 50.0694, "lng": 8.2422, "category": "coworking", "desc": "Coworking space"},
            
            # Offenbach (5 places)
            {"name": "Café Sommergarten", "city": "Offenbach am Main", "address": "Bernardstraße 71", "lat": 50.0989, "lng": 8.7631, "category": "cafe", "desc": "Garden café"},
            {"name": "Isenburger Schloss", "city": "Offenbach am Main", "address": "Schloßstraße 54", "lat": 50.0972, "lng": 8.7606, "category": "landmark", "desc": "Historic castle"},
            {"name": "Ledermuseum", "city": "Offenbach am Main", "address": "Frankfurter Str. 86", "lat": 50.1042, "lng": 8.7619, "category": "museum", "desc": "Leather museum"},
            {"name": "Mainufer Café", "city": "Offenbach am Main", "address": "Mainstraße 12", "lat": 50.1017, "lng": 8.7611, "category": "cafe", "desc": "Riverside café"},
            {"name": "Büsing Palais", "city": "Offenbach am Main", "address": "Herrnstraße 61", "lat": 50.1000, "lng": 8.7639, "category": "venue", "desc": "Cultural venue"},
            
            # Marburg (5 places)
            {"name": "Café Barfuß", "city": "Marburg", "address": "Barfüßerstraße 33", "lat": 50.8097, "lng": 8.7714, "category": "cafe", "desc": "Student café"},
            {"name": "Marburger Schloss", "city": "Marburg", "address": "Schlossberg", "lat": 50.8147, "lng": 8.7664, "category": "landmark", "desc": "Medieval castle"},
            {"name": "Uni Bibliothek Marburg", "city": "Marburg", "address": "Wilhelm-Röpke-Straße 4", "lat": 50.8078, "lng": 8.7739, "category": "library", "desc": "University library"},
            {"name": "Oberstadt Café", "city": "Marburg", "address": "Markt 18", "lat": 50.8122, "lng": 8.7692, "category": "cafe", "desc": "Old town café"},
            {"name": "Alte Universität", "city": "Marburg", "address": "Lahntor 3", "lat": 50.8106, "lng": 8.7711, "category": "landmark", "desc": "Historic university building"}
        ]
        
        places = []
        for place_data in places_data:
            place = Place(
                name=place_data["name"],
                address=place_data["address"],
                city=place_data["city"],
                latitude=place_data["lat"],
                longitude=place_data["lng"],
                category=place_data["category"],
                description=place_data["desc"],
                is_active=True
            )
            db.add(place)
            places.append(place)
        
        db.commit()
        print(f"✅ Created {len(places)} mock places in Hessen")
        
        # Create mock checkins with different durations
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
        
        # Create 15-20 active checkins
        now = datetime.utcnow()
        checkins = []
        
        for i in range(20):
            user = random.choice(users)
            place = random.choice(places)
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
        print(f"✅ Created {len(checkins)} mock checkins")
        
        print("\n🎉 Mock data created successfully!")
        print(f"   - {len(users)} users with profiles")
        print(f"   - {len(places)} places in Hessen")
        print(f"   - {len(checkins)} active checkins")
        print("\n📍 Cities covered:")
        cities = set([p.city for p in places])
        for city in cities:
            count = len([p for p in places if p.city == city])
            print(f"   - {city}: {count} places")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_hessen_mock_data()
