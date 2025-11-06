#!/usr/bin/env python3
"""
Test authentication and protected endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_auth():
    print_section("🔐 Testing Authentication System")
    
    # Test 1: Register a new user
    print("\n1️⃣ Register New User")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "username": "testuser",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("   ✅ Registration successful!")
            user = response.json()
            print(f"   - User ID: {user['id']}")
            print(f"   - Email: {user['email']}")
            print(f"   - Username: {user['username']}")
        elif response.status_code == 400:
            print("   ℹ️  User already exists (that's ok)")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None
    
    # Test 2: Login with existing user
    print("\n2️⃣ Login with Existing User")
    login_data = {
        "email": "max.mueller@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/json", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("   ✅ Login successful!")
            print(f"   - Token: {token[:30]}...")
            return token
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   - Response: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_protected_endpoints(token):
    print_section("🔒 Testing Protected Endpoints")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Get current user
    print("\n1️⃣ Get Current User (/auth/me)")
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print("   ✅ Success!")
            print(f"   - Name: {user['full_name']}")
            print(f"   - Email: {user['email']}")
            print(f"   - Username: {user['username']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Create a check-in
    print("\n2️⃣ Create Check-in (Protected)")
    checkin_data = {
        "place_id": 1,
        "message": "Testing the API! Great place to work 💻"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/checkins/",
            headers=headers,
            json=checkin_data
        )
        if response.status_code == 201:
            checkin = response.json()
            print("   ✅ Check-in created!")
            print(f"   - Check-in ID: {checkin['id']}")
            print(f"   - Place ID: {checkin['place_id']}")
            print(f"   - Message: {checkin['message']}")
            print(f"   - Status: {checkin['status']}")
            return checkin['id']
        elif response.status_code == 400:
            error = response.json()
            print(f"   ℹ️  {error['detail']}")
            # Get existing checkin
            response = requests.get(f"{BASE_URL}/checkins/my", headers=headers)
            if response.status_code == 200:
                checkins = response.json()
                if checkins:
                    return checkins[0]['id']
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return None

def test_checkin_operations(token, checkin_id):
    if not checkin_id:
        print("\n⚠️  Skipping check-in operations (no active check-in)")
        return
    
    print_section("📍 Testing Check-in Operations")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Get my check-ins
    print("\n1️⃣ Get My Check-ins")
    try:
        response = requests.get(f"{BASE_URL}/checkins/my", headers=headers)
        if response.status_code == 200:
            checkins = response.json()
            print(f"   ✅ Found {len(checkins)} check-in(s)")
            for checkin in checkins[:3]:
                print(f"   - Place ID: {checkin['place_id']}, Status: {checkin['status']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: End check-in
    print(f"\n2️⃣ End Check-in (ID: {checkin_id})")
    try:
        response = requests.post(
            f"{BASE_URL}/checkins/{checkin_id}/end",
            headers=headers
        )
        if response.status_code == 200:
            checkin = response.json()
            print("   ✅ Check-in ended!")
            print(f"   - Status: {checkin['status']}")
            print(f"   - Check-out time: {checkin['check_out_time']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_without_auth():
    print_section("🚫 Testing Without Authentication")
    
    # Try to create checkin without token
    print("\n1️⃣ Try to Create Check-in Without Auth")
    checkin_data = {
        "place_id": 1,
        "message": "This should fail"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/checkins/", json=checkin_data)
        if response.status_code == 401:
            print("   ✅ Correctly blocked (401 Unauthorized)")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Try to get /me without token
    print("\n2️⃣ Try to Access /auth/me Without Auth")
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        if response.status_code == 401:
            print("   ✅ Correctly blocked (401 Unauthorized)")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("\n" + "🔐" * 30)
    print("     ZUTREFFEN AUTHENTICATION TEST SUITE")
    print("🔐" * 30)
    
    try:
        # Test authentication
        token = test_auth()
        
        if not token:
            print("\n❌ Cannot proceed without valid token")
            return
        
        # Test protected endpoints
        checkin_id = test_protected_endpoints(token)
        
        # Test checkin operations
        test_checkin_operations(token, checkin_id)
        
        # Test without auth
        test_without_auth()
        
        print_section("✅ All Authentication Tests Complete!")
        print("\n📚 Try the interactive docs:")
        print("   http://localhost:8001/docs")
        print("\n🔑 You can now authenticate in Swagger UI:")
        print("   1. Click 'Authorize' button")
        print("   2. Login with: max.mueller@example.com / password123")
        print("   3. Try protected endpoints!\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API.")
        print("   Make sure the server is running:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001\n")

if __name__ == "__main__":
    main()
