# OpenQuiz Server

A Flask-based server for managing game rooms and quizzes with flexible content types.

## Features

### Room Management
- 6-digit numerical room codes for easy sharing
- Thread-safe room management
- Automatic room expiry (30 minutes)
- Player capacity limits (configurable, default 10 players)
- Duplicate player name prevention

### Quiz System
- Flexible quiz creation from JSON
- Multiple content types: text, image, video, audio
- In-memory storage with optional file persistence
- Solution visibility control (client vs. server)
- Metadata support (difficulty, points, categories, etc.)
- Thread-safe quiz management

### General
- Comprehensive error handling
- RESTful API design
- Health check endpoint

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

The server will start on `http://localhost:4230`

## API Endpoints

### Room Management
- `POST /room/create` - Create a new game room
- `POST /room/join` - Join an existing room
- `GET /room/<room_code>` - Get room details
- `GET /rooms` - List all active rooms

### Quiz Management
- `POST /quiz/create` - Create a new quiz from JSON
- `GET /quiz/<quiz_id>` - Get a quiz by ID
- `GET /quizzes` - List all quizzes

### General
- `GET /health` - Health check endpoint

## Documentation

- **[Getting Started](docs/getting-started.md)** - Installation, setup, and configuration
- **[Room API](docs/room-api.md)** - Room management endpoints and examples
- **[Quiz API](docs/quiz-api.md)** - Quiz creation, retrieval, and item types

## Quick Examples

### Create a Room

```bash
curl -X POST http://localhost:4230/room/create \
  -H "Content-Type: application/json" \
  -d '{"host_name": "Player1", "max_players": 4}'
```

### Create a Quiz

```bash
curl -X POST http://localhost:4230/quiz/create \
  -H "Content-Type: application/json" \
  -d '{
    "question": {"type": "text", "content": "What is 2+2?"},
    "answers": [
      {"type": "text", "content": "3"},
      {"type": "text", "content": "4"},
      {"type": "text", "content": "5"}
    ],
    "correct_index": 1,
    "metadata": {"difficulty": "easy", "points": 10}
  }'
```

### Health Check

```bash
curl http://localhost:4230/health
```

## Project Structure

```
openquiz-server/
├── server.py                    # Main Flask server
├── templates/                   # Quiz template system
│   ├── __init__.py
│   ├── items.py                # Item types (Text, Image, Video, Audio)
│   ├── quiz.py                 # QuizTemplate and Registry
│   └── README.md               # Template system documentation
├── docs/                        # API documentation
│   ├── getting-started.md      # Setup and configuration
│   ├── room-api.md             # Room endpoints
│   └── quiz-api.md             # Quiz endpoints
├── examples.py                  # Usage examples
├── test_quiz_create_api.py     # API tests
└── data/                        # Quiz storage (when save_to_file=true)
    └── quizzes/
```

## Testing

Run the test suite:

```bash
python test_quiz_create_api.py
```

## Configuration

Edit `server.py` to configure:

```python
ROOM_EXPIRY_MINUTES = 30         # Room expiration time
MAX_PLAYERS_PER_ROOM = 10        # Maximum players per room
QUIZ_STORAGE_DIR = 'data/quizzes'  # Quiz file storage directory
```

## Production Considerations

This server is ready for development and testing. For production use, consider adding:

- Database persistence (PostgreSQL, Redis)
- Authentication/authorization
- WebSocket support for real-time updates
- Rate limiting
- HTTPS support
- Production WSGI server (Gunicorn, uWSGI)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
