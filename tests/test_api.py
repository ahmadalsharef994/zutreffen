#!/usr/bin/env python3
"""Test script to verify API endpoints are working with real data"""
import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

def test_api():
    print("=" * 60)
    print("🧪 Testing Zutreffen API Endpoints")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1️⃣ Testing Health Endpoint...")
    r = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    
    # Test places endpoint
    print("\n2️⃣ Testing Places Endpoint...")
    r = requests.get(f"{BASE_URL}/places/")
    print(f"   Status: {r.status_code}")
    places = r.json()
    print(f"   Total places: {len(places)}")
    if places:
        print(f"\n   Example place:")
        example = places[0]
        print(f"   - Name: {example['name']}")
        print(f"   - City: {example['city']}")
        print(f"   - Category: {example['category']}")
        print(f"   - Coordinates: {example['latitude']}, {example['longitude']}")
    
    # Test users endpoint
    print("\n3️⃣ Testing Users Endpoint...")
    r = requests.get(f"{BASE_URL}/users/")
    print(f"   Status: {r.status_code}")
    users = r.json()
    print(f"   Total users: {len(users)}")
    if users:
        print(f"\n   Example user:")
        example = users[0]
        print(f"   - Name: {example['full_name']}")
        print(f"   - Email: {example['email']}")
        print(f"   - Bio: {example['bio']}")
    
    # Test checkins endpoint
    print("\n4️⃣ Testing Check-ins Endpoint...")
    r = requests.get(f"{BASE_URL}/checkins/")
    print(f"   Status: {r.status_code}")
    checkins = r.json()
    print(f"   Total active check-ins: {len(checkins)}")
    if checkins:
        print(f"\n   Example check-in:")
        example = checkins[0]
        print(f"   - User ID: {example['user_id']}")
        print(f"   - Place ID: {example['place_id']}")
        print(f"   - Message: {example['message']}")
        print(f"   - Status: {example['status']}")
    
    # Test filtering by city
    print("\n5️⃣ Testing Places Filter (Berlin)...")
    r = requests.get(f"{BASE_URL}/places/?city=Berlin")
    berlin_places = r.json()
    print(f"   Places in Berlin: {len(berlin_places)}")
    for place in berlin_places:
        print(f"   - {place['name']}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n📚 API Documentation available at:")
    print("   http://localhost:8001/docs")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API.")
        print("   Make sure the server is running:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")
