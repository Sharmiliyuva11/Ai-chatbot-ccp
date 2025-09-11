#!/usr/bin/env python3
"""
Debug script to test profile update functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from models.user_model import User
import json

def test_profile_update():
    print("🔍 Debugging Profile Update Issue")
    print("=" * 50)

    # Test 1: Check if test user exists
    print("\n1. Checking if test user exists...")
    test_user = User.find_by_email("test@test.com")
    if test_user:
        print(f"✅ Test user found: {test_user['name']} (ID: {test_user['_id']})")
        user_id = str(test_user['_id'])
    else:
        print("❌ Test user not found")
        return

    # Test 2: Test update_user method directly
    print("\n2. Testing User.update_user method directly...")
    test_update_data = {
        'name': 'Updated Test User',
        'phone': '+1234567890',
        'location': 'Test City',
        'bio': 'Updated bio for debugging'
    }

    print(f"📤 Update data: {json.dumps(test_update_data, indent=2)}")

    update_result = User.update_user(user_id, test_update_data)
    print(f"📊 Update result: {update_result}")

    if update_result:
        print("✅ User.update_user returned True")

        # Test 3: Verify the update persisted
        print("\n3. Verifying update persisted...")
        updated_user = User.find_by_id(user_id)
        if updated_user:
            print("✅ Updated user data:")
            print(f"   Name: {updated_user.get('name')}")
            print(f"   Phone: {updated_user.get('phone')}")
            print(f"   Location: {updated_user.get('location')}")
            print(f"   Bio: {updated_user.get('bio')}")
        else:
            print("❌ Could not retrieve updated user")
    else:
        print("❌ User.update_user returned False")

    # Test 4: Test with empty update data
    print("\n4. Testing with empty update data...")
    empty_update_result = User.update_user(user_id, {})
    print(f"📊 Empty update result: {empty_update_result}")

    # Test 5: Test with invalid user ID
    print("\n5. Testing with invalid user ID...")
    invalid_update_result = User.update_user("invalid_id", test_update_data)
    print(f"📊 Invalid ID update result: {invalid_update_result}")

    print("\n" + "=" * 50)
    print("🔍 Debug complete")

if __name__ == "__main__":
    test_profile_update()
