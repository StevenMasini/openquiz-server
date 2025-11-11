"""
Test script for the matchmaking server API
"""

import requests
import json

BASE_URL = "http://localhost:4230"

def test_health():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_create_room():
    """Test room creation"""
    print("Testing /room/create endpoint...")
    data = {
        "host_name": "TestPlayer1",
        "max_players": 4
    }
    response = requests.post(
        f"{BASE_URL}/room/create",
        headers={"Content-Type": "application/json"},
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

    if response.status_code == 201:
        return response.json()['room_code']
    return None

def test_join_room(room_code):
    """Test joining a room"""
    print(f"Testing /room/join endpoint with code {room_code}...")
    data = {
        "room_code": room_code,
        "player_name": "TestPlayer2"
    }
    response = requests.post(
        f"{BASE_URL}/room/join",
        headers={"Content-Type": "application/json"},
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_get_room(room_code):
    """Test getting room info"""
    print(f"Testing /room/{room_code} endpoint...")
    response = requests.get(f"{BASE_URL}/room/{room_code}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_list_rooms():
    """Test listing all rooms"""
    print("Testing /rooms endpoint...")
    response = requests.get(f"{BASE_URL}/rooms")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("Matchmaking Server API Tests")
    print("=" * 50)
    print()

    try:
        # Test health check
        if not test_health():
            print("❌ Server is not healthy!")
            exit(1)

        # Test room creation
        room_code = test_create_room()
        if not room_code:
            print("❌ Failed to create room!")
            exit(1)

        # Test joining room
        test_join_room(room_code)

        # Test getting room info
        test_get_room(room_code)

        # Test listing rooms
        test_list_rooms()

        print("=" * 50)
        print("✅ All tests completed!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 4230")
    except Exception as e:
        print(f"❌ Error: {e}")
