# Room API Documentation

The Room API provides endpoints for creating and managing game rooms with 6-digit codes.

## Endpoints

### POST /room/create

Creates a new game room with a unique 6-digit code.

**Request Body** (optional):

```json
{
  "host_name": "Player1",
  "max_players": 10
}
```

**Parameters:**
- `host_name` (string, optional): Name of the room host. Default: "Host"
- `max_players` (integer, optional): Maximum number of players allowed. Default: 10

**Example:**

```bash
curl -X POST http://localhost:4230/room/create \
  -H "Content-Type: application/json" \
  -d '{"host_name": "Player1", "max_players": 4}'
```

**Response (201 Created):**

```json
{
  "room_code": "123456",
  "host_name": "Player1",
  "created_at": "2025-11-18T12:00:00",
  "expires_at": "2025-11-18T12:30:00",
  "max_players": 4
}
```

---

### POST /room/join

Join an existing game room using a room code.

**Request Body:**

```json
{
  "room_code": "123456",
  "player_name": "Player2"
}
```

**Parameters:**
- `room_code` (string, required): 6-digit room code
- `player_name` (string, required): Name of the player joining

**Example:**

```bash
curl -X POST http://localhost:4230/room/join \
  -H "Content-Type: application/json" \
  -d '{"room_code": "123456", "player_name": "Player2"}'
```

**Response (200 OK):**

```json
{
  "room_code": "123456",
  "player_name": "Player2",
  "players": ["Player1", "Player2"],
  "host_name": "Player1",
  "player_count": 2,
  "max_players": 4,
  "status": "waiting"
}
```

**Error Responses:**

- `400 Bad Request`: Missing required fields or invalid room code format
- `404 Not Found`: Room not found or expired
- `403 Forbidden`: Room is full
- `409 Conflict`: Player name already exists in room

---

### GET /room/<room_code>

Get information about a specific room.

**Parameters:**
- `room_code` (string, required): 6-digit room code (in URL path)

**Example:**

```bash
curl http://localhost:4230/room/123456
```

**Response (200 OK):**

```json
{
  "room_code": "123456",
  "host_name": "Player1",
  "players": ["Player1", "Player2"],
  "player_count": 2,
  "max_players": 10,
  "status": "waiting",
  "created_at": "2025-11-18T12:00:00",
  "expires_at": "2025-11-18T12:30:00"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid room code format
- `404 Not Found`: Room not found or expired

---

### GET /rooms

List all active rooms.

**Example:**

```bash
curl http://localhost:4230/rooms
```

**Response (200 OK):**

```json
{
  "rooms": [
    {
      "room_code": "123456",
      "host_name": "Player1",
      "player_count": 2,
      "max_players": 10,
      "status": "waiting"
    },
    {
      "room_code": "789012",
      "host_name": "Player3",
      "player_count": 1,
      "max_players": 4,
      "status": "waiting"
    }
  ],
  "total": 2
}
```

---

## Room Features

### Room Codes
- 6-digit numerical codes (e.g., "123456")
- Automatically generated and guaranteed unique
- Easy to share and type

### Room Expiry
- Rooms automatically expire after 30 minutes (configurable)
- Expired rooms are cleaned up automatically
- Expiry time is included in room creation response

### Player Management
- Duplicate player names are prevented within a room
- Room capacity limits are enforced
- First player to create the room becomes the host

### Thread Safety
- All room operations are thread-safe
- Uses locks to prevent race conditions
- Safe for concurrent requests

## Common Use Cases

### Creating a Private Game

```bash
# Host creates a room
curl -X POST http://localhost:4230/room/create \
  -H "Content-Type: application/json" \
  -d '{"host_name": "Alice", "max_players": 2}'

# Host shares the room code (e.g., "123456") with friend

# Friend joins the room
curl -X POST http://localhost:4230/room/join \
  -H "Content-Type: application/json" \
  -d '{"room_code": "123456", "player_name": "Bob"}'
```

### Checking Room Status

```bash
# Get current room information
curl http://localhost:4230/room/123456
```

### Finding Available Rooms

```bash
# List all active rooms
curl http://localhost:4230/rooms
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": "Description of the error"
}
```

Common error scenarios:
- Missing required fields
- Invalid room code format
- Room not found
- Room full
- Duplicate player name
- Expired room
