"""Generate realistic check-in data"""
from datetime import datetime, timedelta
import random

CHECKIN_MESSAGES = [
    "Working on my laptop, feel free to join!",
    "Grabbing coffee and reading. Say hi if you see me!",
    "Looking for someone to practice German with ☕",
    "Open to networking and chatting about startups",
    "Just finished a meeting, staying for another hour",
    "Great atmosphere here! Highly recommend",
    "Anyone want to grab lunch after this?",
    "Quiet spot for focused work",
    "Perfect place for a casual business meeting",
    "Love the vibe here! First time visiting",
    None,  # Some checkins without messages
    None,
    None,
]

def generate_mock_checkins(users, places, num_checkins=30):
    """Generate realistic check-ins"""
    checkins = []
    now = datetime.utcnow()
    
    for i in range(num_checkins):
        # Random user and place
        user = random.choice(users)
        place = random.choice(places)
        
        # Random time in the past week
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        check_in_time = now - timedelta(days=days_ago, hours=hours_ago)
        
        # 70% chance the checkin is still active (no checkout)
        status = "active" if random.random() < 0.7 else "ended"
        check_out_time = None
        
        if status == "ended":
            # Checkout 1-4 hours after checkin
            duration = timedelta(hours=random.randint(1, 4))
            check_out_time = check_in_time + duration
        
        checkin = {
            "user_id": user.id,
            "place_id": place.id,
            "status": status,
            "message": random.choice(CHECKIN_MESSAGES),
            "check_in_time": check_in_time,
            "check_out_time": check_out_time,
        }
        checkins.append(checkin)
    
    return checkins
