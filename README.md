# OpenQuiz

## Features

### Main Endpoints

1. POST /room/create - Creates a new game room with a 6-digit code
2. POST /room/join - Join an existing room using the code
3. GET /room/<room_code> - Get room details
4. PUT /room/<room_code> - Update room status
5. GET /rooms - List all active rooms
6. GET /health - Health check endpoint

### Key Features

- 6-digit numerical room codes (e.g., "123456")
- Thread-safe room management
- Automatic room expiry (30 minutes)
- Duplicate player name prevention
- Room capacity limits (configurable, default 10 players)
- Comprehensive error handling

### Getting Started

Install dependencies:
`pip install -r requirements.txt`

Run the server:
`python server.py`

The server will start on `http://localhost:5000`

### API Usage Examples

#### Create a room

```curl
curl -X POST http://localhost:5000/room/create \
  -H "Content-Type: application/json" \
  -d '{"host_name": "Player1", "max_players": 4}'
```

Response

```json

{
  "room_code": "123456",
  "host_name": "Player1",
  "created_at": "2025-11-10T12:00:00",
  "expires_at": "2025-11-10T12:30:00",
  "max_players": 4
}
```

#### Join a room

```curl
curl -X POST http://localhost:5000/room/join \
  -H "Content-Type: application/json" \
  -d '{"room_code": "123456", "player_name": "Player2"}'
```

Response

```json
  {
    "room_code": "123456",
    "player_name": "Player2",
    "players": ["Player1", "Player2"],
    "host_name": "Player1",
    "player_count": 2,
    "max_players": 4,
    "status": "pending"
  }
```

#### Update room status

```curl
curl -X PUT http://localhost:5000/room/123456 \
  -H "Content-Type: application/json" \
  -d '{"status": "ready"}'
```

Response

```json
{
  "room_code": "123456",
  "status": "ready",
  "message": "Room status updated successfully"
}
```

Valid statuses: `pending`, `ready`, `playing`, `finished`

## What's left to do

The server is production-ready for development and testing. For production use, consider adding:

- Database persistence (PostgreSQL, Redis)
- Authentication/authorization
- WebSocket support for real-time updates
- Rate limiting
- HTTPS support