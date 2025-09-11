#!/usr/bin/env python3

from services.local_support_service import LocalSupportService

def test_local_support():
    service = LocalSupportService()

    print("=== Testing Local Support Service ===\n")

    # Test Hyderabad
    print("Testing Hyderabad search...")
    result = service.search_mental_health_services('hyderabad')
    print(f"Success: {result['success']}")
    print(f"Total results: {result['total']}")
    if result['results']:
        print(f"First result: {result['results'][0]['name']}")
    print()

    # Test Delhi
    print("Testing Delhi search...")
    result2 = service.search_mental_health_services('delhi')
    print(f"Success: {result2['success']}")
    print(f"Total results: {result2['total']}")
    if result2['results']:
        print(f"First result: {result2['results'][0]['name']}")
    print()

    # Test Vellore
    print("Testing Vellore search...")
    result3 = service.search_mental_health_services('vellore')
    print(f"Success: {result3['success']}")
    print(f"Total results: {result3['total']}")
    print()

    # Show supported locations
    print("Supported locations:")
    locations = service.get_supported_locations()
    for loc in locations:
        print(f"  - {loc}")

    # Test city data mapping
    print("\nTesting city data mapping...")
    city_services = service._get_city_mental_health_services('hyderabad')
    print(f"Hyderabad services found: {len(city_services)}")

    city_services2 = service._get_city_mental_health_services('vellore')
    print(f"Vellore services found: {len(city_services2)}")

if __name__ == "__main__":
    test_local_support()
