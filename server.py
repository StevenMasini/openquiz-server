"""
Matchmaking Server for Game Rooms
Provides HTTP endpoints to create and join game rooms with 6-digit codes
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random
import string
from typing import Dict, List, Optional
import threading
import uuid
from templates import QuizTemplate

app = Flask(__name__)

# In-memory storage for game rooms
game_rooms: Dict[str, dict] = {}
room_lock = threading.Lock()

# In-memory storage for quizzes
quizzes: Dict[str, dict] = {}
quiz_lock = threading.Lock()

# Configuration
ROOM_EXPIRY_MINUTES = 30
MAX_PLAYERS_PER_ROOM = 10
QUIZ_STORAGE_DIR = 'data/quizzes'


def generate_room_code() -> str:
    """Generate a unique 6-digit numerical room code"""
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        if code not in game_rooms:
            return code


def cleanup_expired_rooms():
    """Remove rooms that have expired"""
    current_time = datetime.now()
    with room_lock:
        expired_codes = [
            code for code, room in game_rooms.items()
            if current_time > room['expires_at']
        ]
        for code in expired_codes:
            del game_rooms[code]
        return len(expired_codes)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/room/create', methods=['POST'])
def create_room():
    """
    Create a new game room

    Request body (optional):
    {
        "host_name": "Player1",
        "max_players": 10
    }

    Response:
    {
        "room_code": "123456",
        "host_name": "Player1",
        "created_at": "2025-11-10T12:00:00",
        "expires_at": "2025-11-10T12:30:00",
        "max_players": 10
    }
    """
    cleanup_expired_rooms()

    data = request.get_json() or {}
    host_name = data.get('host_name', 'Host')
    max_players = min(data.get('max_players', MAX_PLAYERS_PER_ROOM), MAX_PLAYERS_PER_ROOM)

    room_code = generate_room_code()
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=ROOM_EXPIRY_MINUTES)

    with room_lock:
        game_rooms[room_code] = {
            'code': room_code,
            'host_name': host_name,
            'players': [host_name],
            'created_at': created_at,
            'expires_at': expires_at,
            'max_players': max_players,
            'status': 'waiting'
        }

    return jsonify({
        'room_code': room_code,
        'host_name': host_name,
        'created_at': created_at.isoformat(),
        'expires_at': expires_at.isoformat(),
        'max_players': max_players
    }), 201


@app.route('/room/join', methods=['POST'])
def join_room():
    """
    Join an existing game room

    Request body:
    {
        "room_code": "123456",
        "player_name": "Player2"
    }

    Response:
    {
        "room_code": "123456",
        "player_name": "Player2",
        "players": ["Player1", "Player2"],
        "host_name": "Player1",
        "status": "waiting"
    }
    """
    cleanup_expired_rooms()

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    room_code = data.get('room_code', '').strip()
    player_name = data.get('player_name', '').strip()

    if not room_code:
        return jsonify({'error': 'room_code is required'}), 400

    if not player_name:
        return jsonify({'error': 'player_name is required'}), 400

    # Validate room code format (6 digits)
    if not (len(room_code) == 6 and room_code.isdigit()):
        return jsonify({'error': 'Invalid room code format. Must be 6 digits'}), 400

    with room_lock:
        room = game_rooms.get(room_code)

        if not room:
            return jsonify({'error': 'Room not found or expired'}), 404

        if player_name in room['players']:
            return jsonify({'error': 'Player name already exists in this room'}), 409

        if len(room['players']) >= room['max_players']:
            return jsonify({'error': 'Room is full'}), 403

        room['players'].append(player_name)

        return jsonify({
            'room_code': room_code,
            'player_name': player_name,
            'players': room['players'],
            'host_name': room['host_name'],
            'player_count': len(room['players']),
            'max_players': room['max_players'],
            'status': room['status']
        }), 200


@app.route('/room/<room_code>', methods=['GET'])
def get_room_info(room_code: str):
    """
    Get information about a specific room

    Response:
    {
        "room_code": "123456",
        "host_name": "Player1",
        "players": ["Player1", "Player2"],
        "player_count": 2,
        "max_players": 10,
        "status": "waiting",
        "created_at": "2025-11-10T12:00:00",
        "expires_at": "2025-11-10T12:30:00"
    }
    """
    cleanup_expired_rooms()

    if not (len(room_code) == 6 and room_code.isdigit()):
        return jsonify({'error': 'Invalid room code format. Must be 6 digits'}), 400

    with room_lock:
        room = game_rooms.get(room_code)

        if not room:
            return jsonify({'error': 'Room not found or expired'}), 404

        return jsonify({
            'room_code': room['code'],
            'host_name': room['host_name'],
            'players': room['players'],
            'player_count': len(room['players']),
            'max_players': room['max_players'],
            'status': room['status'],
            'created_at': room['created_at'].isoformat(),
            'expires_at': room['expires_at'].isoformat()
        }), 200


@app.route('/rooms', methods=['GET'])
def list_rooms():
    """
    List all active rooms

    Response:
    {
        "rooms": [...],
        "total": 5
    }
    """
    cleanup_expired_rooms()

    with room_lock:
        rooms_list = [
            {
                'room_code': room['code'],
                'host_name': room['host_name'],
                'player_count': len(room['players']),
                'max_players': room['max_players'],
                'status': room['status']
            }
            for room in game_rooms.values()
        ]

    return jsonify({
        'rooms': rooms_list,
        'total': len(rooms_list)
    }), 200


# ============================================================================
# Quiz Endpoints
# ============================================================================

@app.route('/quiz/create', methods=['POST'])
def create_quiz():
    """
    Create a new quiz from JSON data

    Request body:
    {
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
            "points": 10
        }
    }

    Optional query parameter:
    - save_to_file: If true, saves the quiz to a JSON file (default: false)

    Response:
    {
        "quiz_id": "uuid-here",
        "message": "Quiz created successfully",
        "saved_to_file": false,
        "file_path": null,
        "created_at": "2025-11-18T12:00:00"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    # Validate required fields
    if 'question' not in data:
        return jsonify({'error': 'question is required'}), 400
    if 'answers' not in data:
        return jsonify({'error': 'answers is required'}), 400
    if 'correct_index' not in data:
        return jsonify({'error': 'correct_index is required'}), 400

    try:
        # Create QuizTemplate from JSON data
        quiz = QuizTemplate.from_dict(data)

        # Validate the quiz
        if not quiz.validate():
            return jsonify({'error': 'Invalid quiz structure'}), 400

        # Generate unique quiz ID
        quiz_id = str(uuid.uuid4())
        created_at = datetime.now()

        # Store in memory
        with quiz_lock:
            quizzes[quiz_id] = {
                'id': quiz_id,
                'quiz': quiz,
                'created_at': created_at,
                'metadata': quiz.metadata
            }

        # Optionally save to file
        save_to_file = request.args.get('save_to_file', 'false').lower() == 'true'
        file_path = None

        if save_to_file:
            import os
            os.makedirs(QUIZ_STORAGE_DIR, exist_ok=True)
            file_path = f"{QUIZ_STORAGE_DIR}/{quiz_id}.json"
            quiz.to_json_file(file_path, include_solution=True)

        return jsonify({
            'quiz_id': quiz_id,
            'message': 'Quiz created successfully',
            'saved_to_file': save_to_file,
            'file_path': file_path,
            'created_at': created_at.isoformat(),
            'question_preview': data['question'].get('content', 'N/A'),
            'answer_count': len(data['answers'])
        }), 201

    except ValueError as e:
        return jsonify({'error': f'Invalid quiz data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create quiz: {str(e)}'}), 500


@app.route('/quiz/<quiz_id>', methods=['GET'])
def get_quiz(quiz_id: str):
    """
    Get a quiz by ID

    Query parameters:
    - include_solution: If true, includes the correct_index (default: false)

    Response:
    {
        "quiz_id": "uuid-here",
        "quiz": {...},
        "created_at": "2025-11-18T12:00:00",
        "metadata": {...}
    }
    """
    with quiz_lock:
        quiz_data = quizzes.get(quiz_id)

        if not quiz_data:
            return jsonify({'error': 'Quiz not found'}), 404

        include_solution = request.args.get('include_solution', 'false').lower() == 'true'

        return jsonify({
            'quiz_id': quiz_id,
            'quiz': quiz_data['quiz'].to_dict(include_solution=include_solution),
            'created_at': quiz_data['created_at'].isoformat(),
            'metadata': quiz_data['metadata']
        }), 200


@app.route('/quizzes', methods=['GET'])
def list_quizzes():
    """
    List all quizzes

    Response:
    {
        "quizzes": [...],
        "total": 5
    }
    """
    with quiz_lock:
        quiz_list = [
            {
                'quiz_id': quiz_id,
                'created_at': quiz_data['created_at'].isoformat(),
                'metadata': quiz_data['metadata']
            }
            for quiz_id, quiz_data in quizzes.items()
        ]

    return jsonify({
        'quizzes': quiz_list,
        'total': len(quiz_list)
    }), 200


if __name__ == '__main__':
    print("🎮 Matchmaking Server Starting...")
    print(f"📝 Room expiry: {ROOM_EXPIRY_MINUTES} minutes")
    print(f"👥 Max players per room: {MAX_PLAYERS_PER_ROOM}")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=4230)
