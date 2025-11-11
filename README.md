# OpenQuiz

## Features

### Main Endpoints

1. POST /room/create - Creates a new game room with a 6-digit code
2. POST /room/join - Join an existing room using the code
3. GET /room/ - Get room details
4. GET /rooms - List all active rooms
5. GET /health - Health check endpoint

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
    "status": "waiting"
  }
```

## What's left to do

The server is production-ready for development and testing. For production use, consider adding:

- Database persistence (PostgreSQL, Redis)
- Authentication/authorization
- WebSocket support for real-time updates
- Rate limiting
- HTTPS support

## Perfect! Let me show you a summary of what I've implemented:

  📦 Implementation Complete!

  I've created a flexible quiz template system using ABC with Item composition and HTML rendering.
  Here's what was built:

  📁 File Structure

  openquiz-server/
  ├── templates/
  │   ├── __init__.py          # Package exports
  │   ├── items.py             # Item ABC + concrete implementations
  │   ├── quiz.py              # QuizTemplate + Registry
  │   └── README.md            # Complete documentation
  ├── examples.py              # 10+ usage examples
  ├── server_integration_example.py  # Flask API integration
  └── test_quiz_api.py         # API endpoint tests

  🏗️ Architecture

  Item (ABC)
  ├── TextItem        # <p>text</p>
  ├── ImageItem       # <img src="..." />
  ├── VideoItem       # <video>...</video>
  └── AudioItem       # <audio>...</audio>

  QuizTemplate
  ├── question: Item           # Any Item type
  ├── answers: List[Item]      # List of any Item types
  ├── correct_index: int       # Index of correct answer
  └── metadata: Dict           # Points, time, difficulty, etc.

  ✨ Key Features

  1. Flexible composition - Mix any content types
  2. HTML rendering - quiz.render() produces ready-to-use HTML
  3. Security - Automatic HTML escaping prevents XSS
  4. Variable answers - 4, 6, or any number of answers
  5. Metadata support - Points, time limits, difficulty, categories
  6. Serialization - Save/load from dictionaries/JSON
  7. Registry pattern - Manage multiple quizzes by ID

  🎯 Usage Examples

  Basic 4-answer text quiz:
  quiz = QuizTemplate(
      question=TextItem("What is 2+2?"),
      answers=[TextItem("3"), TextItem("4"), TextItem("5"), TextItem("6")],
      correct_index=1
  )
  html = quiz.render()

  Image question, 6 text answers:
  quiz = QuizTemplate(
      question=ImageItem("https://example.com/flag.png", width="300px"),
      answers=[TextItem(f"Country {i}") for i in range(6)],
      correct_index=2
  )

  Mix any content types:
  quiz = QuizTemplate(
      question=VideoItem("https://example.com/clip.mp4"),
      answers=[ImageItem(f"option{i}.png") for i in range(4)],
      correct_index=0
  )

  🔌 Server Integration

  The server_integration_example.py provides Flask endpoints:

- GET /quiz/list - List all quizzes
- GET /quiz/<id>/html - Get rendered HTML
- GET /quiz/<id>/data - Get structured data
- POST /quiz/<id>/submit - Submit answer & get points
- POST /room/<code>/quiz - Assign quiz to game room

  🧪 Try It Out

# See all examples
  python examples.py

# Start the integration server
  python server_integration_example.py

# Test the API (in another terminal)
  python test_quiz_api.py

  🎨 HTML Output Example

  <div class="quiz-container">
    <div class="quiz-question">
      <p>What is the capital of France?</p>
    </div>
    <div class="quiz-answers">
      <div class="quiz-answer" data-answer-index="0">
        <p>London</p>
      </div>
      <div class="quiz-answer" data-answer-index="1">
        <p>Paris</p>
      </div>
      <!-- ... -->
    </div>
  </div>

  🚀 Server Only Knows the Interface

  def send_quiz_to_player(quiz: QuizTemplate):
      # Server doesn't know if it's text, image, video, etc!
      html = quiz.render()
      send_to_client(html)

  def check_player_answer(quiz: QuizTemplate, answer: int):
      # Works for any quiz type
      return quiz.check_answer(answer)

  The server works purely through the Item interface - it never needs to know what specific types are
  inside!

  📚 Full Documentation

  See templates/README.md for complete API documentation, security notes, and extension examples.

  Your friend's compositional design was great! This gives you maximum flexibility to define any quiz
  template while keeping the server code simple and clean.
