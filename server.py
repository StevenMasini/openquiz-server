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

app = Flask(__name__)

# In-memory storage for game rooms
game_rooms: Dict[str, dict] = {}
room_lock = threading.Lock()

# Configuration
ROOM_EXPIRY_MINUTES = 30
MAX_PLAYERS_PER_ROOM = 10


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


if __name__ == '__main__':
    print("🎮 Matchmaking Server Starting...")
    print(f"📝 Room expiry: {ROOM_EXPIRY_MINUTES} minutes")
    print(f"👥 Max players per room: {MAX_PLAYERS_PER_ROOM}")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
