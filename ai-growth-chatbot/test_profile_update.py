#!/usr/bin/env python3
"""
Test script to verify profile update functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_profile_endpoints():
    """Test profile GET and PUT endpoints"""
    print("🧪 Testing Profile Update Functionality")
    print("=" * 50)

    # Test 1: Health check
    print("\n1. Testing backend health...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return

    # Test 2: Login to get JWT token
    print("\n2. Testing login...")
    login_data = {
        "email": "user",  # Using test user
        "password": "123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                token = data.get('token')
                user_id = data.get('user', {}).get('id')
                print("✅ Login successful")
                print(f"   Token: {token[:20]}...")
                print(f"   User ID: {user_id}")
            else:
                print(f"❌ Login failed: {data.get('message')}")
                return
        else:
            print(f"❌ Login request failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Test 3: Get current profile
    print("\n3. Testing GET profile...")
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user = data.get('user', {})
                print("✅ Profile fetched successfully")
                print(f"   Name: {user.get('name')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Phone: {user.get('phone')}")
                print(f"   Location: {user.get('location')}")
                print(f"   Bio: {user.get('bio')}")
            else:
                print(f"❌ Profile fetch failed: {data.get('message')}")
                return
        else:
            print(f"❌ Profile GET failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Profile GET error: {e}")
        return

    # Test 4: Update profile
    print("\n4. Testing PUT profile update...")
    update_data = {
        "name": "Updated Test User",
        "phone": "+1234567890",
        "location": "Test City, TC",
        "bio": "Updated bio for testing profile functionality",
        "emergencyContact": {
            "name": "Emergency Contact",
            "relationship": "Friend",
            "phone": "+0987654321"
        }
    }

    try:
        response = requests.put(f"{BASE_URL}/auth/profile", json=update_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Profile updated successfully")
                updated_user = data.get('user', {})
                print(f"   Updated Name: {updated_user.get('name')}")
                print(f"   Updated Phone: {updated_user.get('phone')}")
                print(f"   Updated Location: {updated_user.get('location')}")
                print(f"   Updated Bio: {updated_user.get('bio')}")
            else:
                print(f"❌ Profile update failed: {data.get('message')}")
                return
        else:
            print(f"❌ Profile PUT failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Profile PUT error: {e}")
        return

    # Test 5: Verify update persisted
    print("\n5. Verifying update persistence...")
    time.sleep(1)  # Small delay to ensure DB write

    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user = data.get('user', {})
                if (user.get('name') == update_data['name'] and
                    user.get('phone') == update_data['phone'] and
                    user.get('location') == update_data['location']):
                    print("✅ Profile update persisted in database")
                    print("🎉 All tests passed! Profile update functionality is working correctly.")
                else:
                    print("❌ Profile data not persisted correctly")
                    print(f"   Expected name: {update_data['name']}")
                    print(f"   Actual name: {user.get('name')}")
            else:
                print(f"❌ Profile verification failed: {data.get('message')}")
        else:
            print(f"❌ Profile verification GET failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Profile verification error: {e}")

if __name__ == "__main__":
    test_profile_endpoints()
