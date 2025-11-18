# Getting Started

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

Start the server:

```bash
python server.py
```

The server will start on `http://localhost:4230`

You should see output like:

```
🎮 Matchmaking Server Starting...
📝 Room expiry: 30 minutes
👥 Max players per room: 10
==================================================
 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://127.0.0.1:4230
```

## Testing the Server

### Health Check

Verify the server is running:

```bash
curl http://localhost:4230/health
```

Expected response:

```json
{
  "status": "healthy",
  "timestamp": "2025-11-18T12:00:00.000000"
}
```

### Run Test Suite

Test the quiz creation API:

```bash
python test_quiz_create_api.py
```

## Configuration

The server configuration can be modified in `server.py`:

```python
# Configuration
ROOM_EXPIRY_MINUTES = 30        # Room expiration time
MAX_PLAYERS_PER_ROOM = 10       # Maximum players per room
QUIZ_STORAGE_DIR = 'data/quizzes'  # Directory for saved quizzes
```

## Next Steps

- [Room API Documentation](room-api.md) - Learn about room management endpoints
- [Quiz API Documentation](quiz-api.md) - Learn about quiz creation and retrieval endpoints

## Troubleshooting

### Port Already in Use

If you see "Address already in use" error:

```bash
# Find and kill the process using port 4230
lsof -ti:4230 | xargs kill -9
```

### Module Not Found

If you see "ModuleNotFoundError":

```bash
# Make sure you've installed dependencies
pip install -r requirements.txt

# Or if using virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Flask Not Found

If Flask is not installed:

```bash
pip install flask
```
