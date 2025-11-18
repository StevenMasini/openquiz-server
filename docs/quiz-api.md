# Quiz API Documentation

The Quiz API provides endpoints for creating, retrieving, and managing quizzes with flexible content types.

## Endpoints

### POST /quiz/create

Creates a new quiz from JSON data.

**Query Parameters:**
- `save_to_file` (boolean, optional): If true, saves the quiz to a JSON file. Default: false

**Request Body:**

```json
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
    "points": 10,
    "category": "geography"
  }
}
```

**Required Fields:**
- `question` (object): The question item
- `answers` (array): List of answer items (minimum 1)
- `correct_index` (integer): Index of the correct answer (0-based)

**Optional Fields:**
- `metadata` (object): Additional quiz metadata (difficulty, points, category, time_limit, etc.)

**Example:**

```bash
curl -X POST http://localhost:4230/quiz/create \
  -H "Content-Type: application/json" \
  -d '{
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
      "points": 10,
      "category": "geography"
    }
  }'
```

**Response (201 Created):**

```json
{
  "quiz_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Quiz created successfully",
  "saved_to_file": false,
  "file_path": null,
  "created_at": "2025-11-18T12:00:00.000000",
  "question_preview": "What is the capital of France?",
  "answer_count": 4
}
```

**Error Responses:**

- `400 Bad Request`: Missing required fields or invalid quiz structure
- `500 Internal Server Error`: Failed to create quiz

---

### POST /quiz/create?save_to_file=true

Creates a quiz and saves it to a JSON file.

**Example:**

```bash
curl -X POST "http://localhost:4230/quiz/create?save_to_file=true" \
  -H "Content-Type: application/json" \
  -d '{
    "question": {
      "type": "text",
      "content": "What is 2 + 2?"
    },
    "answers": [
      {"type": "text", "content": "3"},
      {"type": "text", "content": "4"},
      {"type": "text", "content": "5"},
      {"type": "text", "content": "22"}
    ],
    "correct_index": 1,
    "metadata": {
      "difficulty": "trivial",
      "points": 5
    }
  }'
```

**Response (201 Created):**

```json
{
  "quiz_id": "550e8400-e29b-41d4-a716-446655440001",
  "message": "Quiz created successfully",
  "saved_to_file": true,
  "file_path": "data/quizzes/550e8400-e29b-41d4-a716-446655440001.json",
  "created_at": "2025-11-18T12:00:00.000000",
  "question_preview": "What is 2 + 2?",
  "answer_count": 4
}
```

---

### GET /quiz/<quiz_id>

Retrieves a quiz by ID.

**Query Parameters:**
- `include_solution` (boolean, optional): If true, includes the correct_index. Default: false

**Example (without solution - for clients):**

```bash
curl "http://localhost:4230/quiz/550e8400-e29b-41d4-a716-446655440000?include_solution=false"
```

**Response (200 OK):**

```json
{
  "quiz_id": "550e8400-e29b-41d4-a716-446655440000",
  "quiz": {
    "question": {
      "type": "text",
      "content": "What is the capital of France?",
      "css_class": ""
    },
    "answers": [
      {"type": "text", "content": "London", "css_class": ""},
      {"type": "text", "content": "Paris", "css_class": ""},
      {"type": "text", "content": "Berlin", "css_class": ""},
      {"type": "text", "content": "Madrid", "css_class": ""}
    ],
    "metadata": {
      "difficulty": "easy",
      "points": 10,
      "category": "geography"
    }
  },
  "created_at": "2025-11-18T12:00:00.000000",
  "metadata": {
    "difficulty": "easy",
    "points": 10,
    "category": "geography"
  }
}
```

**Example (with solution - for verification):**

```bash
curl "http://localhost:4230/quiz/550e8400-e29b-41d4-a716-446655440000?include_solution=true"
```

**Response (200 OK):**

```json
{
  "quiz_id": "550e8400-e29b-41d4-a716-446655440000",
  "quiz": {
    "question": {
      "type": "text",
      "content": "What is the capital of France?",
      "css_class": ""
    },
    "answers": [
      {"type": "text", "content": "London", "css_class": ""},
      {"type": "text", "content": "Paris", "css_class": ""},
      {"type": "text", "content": "Berlin", "css_class": ""},
      {"type": "text", "content": "Madrid", "css_class": ""}
    ],
    "correct_index": 1,
    "metadata": {
      "difficulty": "easy",
      "points": 10,
      "category": "geography"
    }
  },
  "created_at": "2025-11-18T12:00:00.000000",
  "metadata": {
    "difficulty": "easy",
    "points": 10,
    "category": "geography"
  }
}
```

**Error Responses:**

- `404 Not Found`: Quiz not found

---

### GET /quizzes

Lists all stored quizzes.

**Example:**

```bash
curl http://localhost:4230/quizzes
```

**Response (200 OK):**

```json
{
  "quizzes": [
    {
      "quiz_id": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2025-11-18T12:00:00.000000",
      "metadata": {
        "difficulty": "easy",
        "points": 10,
        "category": "geography"
      }
    },
    {
      "quiz_id": "550e8400-e29b-41d4-a716-446655440001",
      "created_at": "2025-11-18T12:05:00.000000",
      "metadata": {
        "difficulty": "trivial",
        "points": 5
      }
    }
  ],
  "total": 2
}
```

---

## Item Types

The Quiz API supports multiple content types for questions and answers:

### TextItem

Plain text content.

```json
{
  "type": "text",
  "content": "What is the capital of France?",
  "css_class": ""
}
```

**Fields:**
- `type`: "text"
- `content` (string, required): The text content
- `css_class` (string, optional): CSS class for styling

### ImageItem

Image content.

```json
{
  "type": "image",
  "url": "https://example.com/image.png",
  "alt": "Image description",
  "css_class": "",
  "width": "400px",
  "height": "300px"
}
```

**Fields:**
- `type`: "image"
- `url` (string, required): Image URL
- `alt` (string, optional): Alt text for accessibility
- `css_class` (string, optional): CSS class for styling
- `width` (string, optional): Image width (e.g., "400px", "100%")
- `height` (string, optional): Image height

### VideoItem

Video content.

```json
{
  "type": "video",
  "url": "https://example.com/video.mp4",
  "thumbnail": "https://example.com/thumb.jpg",
  "css_class": "",
  "autoplay": false,
  "controls": true
}
```

**Fields:**
- `type`: "video"
- `url` (string, required): Video URL
- `thumbnail` (string, optional): Poster/thumbnail image URL
- `css_class` (string, optional): CSS class for styling
- `autoplay` (boolean, optional): Auto-play video. Default: false
- `controls` (boolean, optional): Show video controls. Default: true

### AudioItem

Audio content.

```json
{
  "type": "audio",
  "url": "https://example.com/audio.mp3",
  "css_class": "",
  "autoplay": false,
  "controls": true
}
```

**Fields:**
- `type`: "audio"
- `url` (string, required): Audio URL
- `css_class` (string, optional): CSS class for styling
- `autoplay` (boolean, optional): Auto-play audio. Default: false
- `controls` (boolean, optional): Show audio controls. Default: true

---

## Example Quizzes

### Image Question with Text Answers

```bash
curl -X POST http://localhost:4230/quiz/create \
  -H "Content-Type: application/json" \
  -d '{
    "question": {
      "type": "image",
      "url": "https://example.com/flags/france.png",
      "alt": "Flag image",
      "width": "400px"
    },
    "answers": [
      {"type": "text", "content": "France"},
      {"type": "text", "content": "Italy"},
      {"type": "text", "content": "Netherlands"},
      {"type": "text", "content": "Russia"}
    ],
    "correct_index": 0,
    "metadata": {
      "difficulty": "medium",
      "points": 15,
      "category": "flags"
    }
  }'
```

### Video Question

```bash
curl -X POST http://localhost:4230/quiz/create \
  -H "Content-Type: application/json" \
  -d '{
    "question": {
      "type": "video",
      "url": "https://example.com/scene.mp4",
      "controls": true
    },
    "answers": [
      {"type": "text", "content": "New York"},
      {"type": "text", "content": "Los Angeles"},
      {"type": "text", "content": "Chicago"}
    ],
    "correct_index": 1
  }'
```

### Audio Identification Quiz

```bash
curl -X POST http://localhost:4230/quiz/create \
  -H "Content-Type: application/json" \
  -d '{
    "question": {
      "type": "audio",
      "url": "https://example.com/sound.mp3",
      "controls": true
    },
    "answers": [
      {"type": "text", "content": "Piano"},
      {"type": "text", "content": "Guitar"},
      {"type": "text", "content": "Violin"}
    ],
    "correct_index": 2,
    "metadata": {
      "category": "music",
      "difficulty": "hard",
      "points": 20
    }
  }'
```

---

## Quiz Features

### Flexible Content Types
- Mix any item types for questions and answers
- Support for text, images, videos, and audio
- Easy to extend with new item types

### In-Memory Storage
- Fast access to quizzes
- Thread-safe operations
- Unique UUID for each quiz

### File Persistence
- Optional JSON file storage
- Human-readable format
- Easy backup and sharing

### Solution Visibility Control
- Send quizzes to clients without revealing answers
- Include solutions for verification
- Prevent cheating

### Metadata Support
- Attach custom metadata to quizzes
- Common fields: difficulty, points, category, time_limit
- Fully customizable

### Validation
- Automatic validation of quiz structure
- Ensures correct_index is within range
- Validates item types

---

## Common Use Cases

### Creating Quizzes for Clients

```bash
# 1. Create a quiz
QUIZ_ID=$(curl -X POST http://localhost:4230/quiz/create \
  -H "Content-Type: application/json" \
  -d '{"question": {...}, "answers": [...], "correct_index": 1}' \
  | jq -r '.quiz_id')

# 2. Send quiz to client (without solution)
curl "http://localhost:4230/quiz/$QUIZ_ID?include_solution=false"
```

### Verifying Answers

```bash
# Get quiz with solution for server-side verification
curl "http://localhost:4230/quiz/$QUIZ_ID?include_solution=true"
```

### Batch Quiz Creation

```bash
# Save quizzes to files for backup
for quiz_data in quiz1.json quiz2.json quiz3.json; do
  curl -X POST "http://localhost:4230/quiz/create?save_to_file=true" \
    -H "Content-Type: application/json" \
    -d @$quiz_data
done
```

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": "Description of the error"
}
```

Common error scenarios:
- Missing required fields
- Invalid item types
- correct_index out of range
- Empty answers array
- Invalid JSON format
- Quiz not found
