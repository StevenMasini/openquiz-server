"""
Room-related routes for the matchmaking server
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from typing import Dict
import threading

# Create Blueprint for room routes
room_bp = Blueprint('room', __name__)

# These will be injected from server.py
game_rooms: Dict[str, dict] = None
room_lock: threading.Lock = None
ROOM_EXPIRY_MINUTES = None
MAX_PLAYERS_PER_ROOM = None


def init_room_routes(rooms_dict, lock, expiry_minutes, max_players):
    """Initialize the room routes with shared resources"""
    global game_rooms, room_lock, ROOM_EXPIRY_MINUTES, MAX_PLAYERS_PER_ROOM
    game_rooms = rooms_dict
    room_lock = lock
    ROOM_EXPIRY_MINUTES = expiry_minutes
    MAX_PLAYERS_PER_ROOM = max_players


def generate_room_code() -> str:
    """Generate a unique 6-digit numerical room code"""
    import random
    import string
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


@room_bp.route('/room/create', methods=['POST'])
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


@room_bp.route('/room/join', methods=['POST'])
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


@room_bp.route('/room/<room_code>', methods=['GET'])
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


@room_bp.route('/room/<room_code>', methods=['PUT'])
def update_room_status(room_code: str):
    """
    Update the status of a room

    Request body:
    {
        "status": "waiting" | "ready" | "playing" | "finished"
    }

    Response:
    {
        "room_code": "123456",
        "status": "ready",
        "message": "Room status updated successfully"
    }
    """
    cleanup_expired_rooms()

    if not (len(room_code) == 6 and room_code.isdigit()):
        return jsonify({'error': 'Invalid room code format. Must be 6 digits'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    new_status = data.get('status', '').strip()

    # Validate status
    valid_statuses = ['waiting', 'ready', 'playing', 'finished']
    if new_status not in valid_statuses:
        return jsonify({
            'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400

    with room_lock:
        room = game_rooms.get(room_code)

        if not room:
            return jsonify({'error': 'Room not found or expired'}), 404

        room['status'] = new_status

        return jsonify({
            'room_code': room_code,
            'status': new_status,
            'message': 'Room status updated successfully'
        }), 200


@room_bp.route('/rooms', methods=['GET'])
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
