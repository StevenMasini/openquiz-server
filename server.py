"""
Matchmaking Server for Game Rooms
Provides HTTP endpoints to create and join game rooms with 6-digit codes
"""

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from typing import Dict
import threading

# Import room routes
from room_routes import room_bp, init_room_routes

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for game rooms
game_rooms: Dict[str, dict] = {}
room_lock = threading.Lock()

# Configuration
ROOM_EXPIRY_MINUTES = 30
MAX_PLAYERS_PER_ROOM = 10

# Initialize and register room routes
init_room_routes(game_rooms, room_lock, ROOM_EXPIRY_MINUTES, MAX_PLAYERS_PER_ROOM)
app.register_blueprint(room_bp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    print("Matchmaking Server Starting...")
    print(f"Room expiry: {ROOM_EXPIRY_MINUTES} minutes")
    print(f"Max players per room: {MAX_PLAYERS_PER_ROOM}")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=4230)
