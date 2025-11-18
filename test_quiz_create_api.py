#!/usr/bin/env python3
"""
Test script for quiz creation API endpoints
Run the server first: python server.py
Then run this script: python test_quiz_create_api.py
"""

import requests
import json

BASE_URL = "http://localhost:4230"

def test_create_quiz():
    """Test creating a quiz"""
    print("\n" + "="*60)
    print("TEST 1: Create a quiz")
    print("="*60)

    quiz_data = {
        "question": {
            "type": "text",
            "content": "What is the capital of France?"
        },
        "answers": [
            {"type": "text", "content": "London"},
            {"type": "text", "content": "Paris"},
            {"type": "text", "content": "Berlin"},
            {"type": "text", "content": "Madrid"}
        ],
        "correct_index": 1,
        "metadata": {
            "difficulty": "easy",
            "points": 10,
            "category": "geography"
        }
    }

    response = requests.post(f"{BASE_URL}/quiz/create", json=quiz_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("✓ Quiz created successfully!")
        return response.json()['quiz_id']
    else:
        print("✗ Failed to create quiz")
        return None


def test_create_quiz_with_file():
    """Test creating a quiz and saving to file"""
    print("\n" + "="*60)
    print("TEST 2: Create a quiz with file save")
    print("="*60)

    quiz_data = {
        "question": {
            "type": "text",
            "content": "What is 2 + 2?"
        },
        "answers": [
            {"type": "text", "content": "3"},
            {"type": "text", "content": "4"},
            {"type": "text", "content": "5"},
            {"type": "text", "content": "22"}
        ],
        "correct_index": 1,
        "metadata": {
            "difficulty": "trivial",
            "points": 5
        }
    }

    response = requests.post(
        f"{BASE_URL}/quiz/create?save_to_file=true",
        json=quiz_data
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("✓ Quiz created and saved to file!")
        return response.json()['quiz_id']
    else:
        print("✗ Failed to create quiz")
        return None


def test_get_quiz(quiz_id, include_solution=False):
    """Test getting a quiz by ID"""
    print("\n" + "="*60)
    print(f"TEST 3: Get quiz (include_solution={include_solution})")
    print("="*60)

    params = {'include_solution': 'true' if include_solution else 'false'}
    response = requests.get(f"{BASE_URL}/quiz/{quiz_id}", params=params)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        quiz_data = response.json()['quiz']
        has_solution = 'correct_index' in quiz_data
        print(f"✓ Quiz retrieved! Has solution: {has_solution}")
        return True
    else:
        print("✗ Failed to get quiz")
        return False


def test_list_quizzes():
    """Test listing all quizzes"""
    print("\n" + "="*60)
    print("TEST 4: List all quizzes")
    print("="*60)

    response = requests.get(f"{BASE_URL}/quizzes")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        total = response.json()['total']
        print(f"✓ Found {total} quizzes")
        return True
    else:
        print("✗ Failed to list quizzes")
        return False


def test_create_image_quiz():
    """Test creating a quiz with image question"""
    print("\n" + "="*60)
    print("TEST 5: Create quiz with image question")
    print("="*60)

    quiz_data = {
        "question": {
            "type": "image",
            "url": "https://example.com/flags/france.png",
            "alt": "Flag image",
            "width": "400px"
        },
        "answers": [
            {"type": "text", "content": "France"},
            {"type": "text", "content": "Italy"},
            {"type": "text", "content": "Netherlands"},
            {"type": "text", "content": "Russia"}
        ],
        "correct_index": 0,
        "metadata": {
            "difficulty": "medium",
            "points": 15,
            "category": "flags"
        }
    }

    response = requests.post(f"{BASE_URL}/quiz/create", json=quiz_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("✓ Image quiz created successfully!")
        return response.json()['quiz_id']
    else:
        print("✗ Failed to create image quiz")
        return None


def test_invalid_quiz():
    """Test creating an invalid quiz"""
    print("\n" + "="*60)
    print("TEST 6: Create invalid quiz (should fail)")
    print("="*60)

    quiz_data = {
        "question": {
            "type": "text",
            "content": "Invalid quiz"
        },
        "answers": [
            {"type": "text", "content": "Answer 1"}
        ],
        "correct_index": 5  # Invalid: out of range
    }

    response = requests.post(f"{BASE_URL}/quiz/create", json=quiz_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 400:
        print("✓ Invalid quiz correctly rejected!")
        return True
    else:
        print("✗ Invalid quiz was not rejected")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("QUIZ API TEST SUITE")
    print("="*60)
    print(f"Testing server at: {BASE_URL}")

    try:
        # Test health check
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("\n✗ Server is not running or not healthy!")
            print("Please start the server first: python server.py")
            return
        print("✓ Server is healthy")

        # Run tests
        quiz_id1 = test_create_quiz()
        quiz_id2 = test_create_quiz_with_file()

        if quiz_id1:
            test_get_quiz(quiz_id1, include_solution=False)
            test_get_quiz(quiz_id1, include_solution=True)

        test_list_quizzes()
        test_create_image_quiz()
        test_invalid_quiz()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60 + "\n")

    except requests.exceptions.ConnectionError:
        print("\n✗ Could not connect to server!")
        print("Please start the server first: python server.py")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == '__main__':
    main()
