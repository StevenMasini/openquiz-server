"""
Test script for quiz template API endpoints
Run server_integration_example.py first, then run this script
"""

import requests
import json

BASE_URL = "http://localhost:4231"


def test_list_quizzes():
    """Test listing all quizzes"""
    print("\n=== TEST: List Quizzes ===")
    response = requests.get(f"{BASE_URL}/quiz/list")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_quiz_html():
    """Test getting quiz as HTML"""
    print("\n=== TEST: Get Quiz HTML ===")
    response = requests.get(f"{BASE_URL}/quiz/basic_001/html")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Quiz ID: {data['quiz_id']}")
    print(f"Metadata: {data['metadata']}")
    print(f"HTML Preview (first 200 chars): {data['html'][:200]}...")


def test_get_quiz_data():
    """Test getting quiz as structured data"""
    print("\n=== TEST: Get Quiz Data ===")
    response = requests.get(f"{BASE_URL}/quiz/mixed_001/data")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_submit_correct_answer():
    """Test submitting correct answer"""
    print("\n=== TEST: Submit Correct Answer ===")
    response = requests.post(
        f"{BASE_URL}/quiz/basic_001/submit",
        json={"answer": 1, "player_id": "player123"}  # Correct answer is index 1
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_submit_wrong_answer():
    """Test submitting wrong answer"""
    print("\n=== TEST: Submit Wrong Answer ===")
    response = requests.post(
        f"{BASE_URL}/quiz/basic_001/submit",
        json={"answer": 0, "player_id": "player123"}  # Wrong answer
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_assign_quiz_to_room():
    """Test assigning quiz to room"""
    print("\n=== TEST: Assign Quiz to Room ===")
    response = requests.post(
        f"{BASE_URL}/room/123456/quiz",
        json={"quiz_id": "image_001"}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Room Code: {data['room_code']}")
    print(f"Quiz ID: {data['quiz_id']}")
    print(f"Metadata: {data['metadata']}")
    print(f"HTML Preview (first 200 chars): {data['quiz_html'][:200]}...")


def test_six_answer_quiz():
    """Test quiz with 6 answers"""
    print("\n=== TEST: Six Answer Quiz ===")
    response = requests.get(f"{BASE_URL}/quiz/six_answers_001/html")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Quiz ID: {data['quiz_id']}")
    print(f"Has 6 answers: {data['html'].count('data-answer-index') == 6}")


def test_error_cases():
    """Test error handling"""
    print("\n=== TEST: Error Cases ===")

    # Non-existent quiz
    response = requests.get(f"{BASE_URL}/quiz/nonexistent/html")
    print(f"Non-existent quiz status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Invalid answer
    response = requests.post(
        f"{BASE_URL}/quiz/basic_001/submit",
        json={"answer": 999}
    )
    print(f"Invalid answer status: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == '__main__':
    print("="*60)
    print("QUIZ TEMPLATE API TESTS")
    print("="*60)
    print("\nMake sure server_integration_example.py is running on port 4231")
    print("="*60)

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health")
        print(f"\nServer health: {response.json()}")

        # Run tests
        test_list_quizzes()
        test_get_quiz_html()
        test_get_quiz_data()
        test_submit_correct_answer()
        test_submit_wrong_answer()
        test_assign_quiz_to_room()
        test_six_answer_quiz()
        test_error_cases()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to server.")
        print("Please start the server first:")
        print("  python server_integration_example.py")
    except Exception as e:
        print(f"\nERROR: {e}")
