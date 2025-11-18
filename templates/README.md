# Quiz Template System

A flexible, compositional system for defining quiz questions with HTML rendering support.

## Architecture

The system uses the **ABC (Abstract Base Class) pattern** with **Item composition**:

```
Item (ABC)
├── TextItem
├── ImageItem
├── VideoItem
└── AudioItem

QuizTemplate
├── question: Item
├── answers: List[Item]
└── correct_index: int
```

## Key Features

- **Flexible Content**: Mix text, images, videos, and audio in any combination
- **HTML Rendering**: Automatic HTML generation with security (escaping)
- **Variable Answers**: Support for 4, 6, or any number of answers
- **Metadata Support**: Points, time limits, difficulty, categories
- **Serialization**: Convert to/from dictionaries for storage
- **Type Safety**: Full Python type hints
- **Security**: HTML escaping prevents injection attacks

## Quick Start

### Basic Text Quiz

```python
from templates import TextItem, QuizTemplate

quiz = QuizTemplate(
    question=TextItem("What is the capital of France?"),
    answers=[
        TextItem("London"),
        TextItem("Paris"),
        TextItem("Berlin"),
        TextItem("Madrid")
    ],
    correct_index=1,
    metadata={'points': 10, 'time_limit': 30}
)

# Render as HTML
html = quiz.render()

# Check answer
is_correct = quiz.check_answer(1)  # True
```

### Image Question Quiz

```python
from templates import ImageItem, TextItem, QuizTemplate

quiz = QuizTemplate(
    question=ImageItem("https://example.com/flag.png", "Flag", width="300px"),
    answers=[
        TextItem("France"),
        TextItem("Italy"),
        TextItem("Netherlands"),
        TextItem("Russia")
    ],
    correct_index=0
)
```

### Mixed Media Quiz

```python
quiz = QuizTemplate(
    question=TextItem("Which logo is Python?"),
    answers=[
        ImageItem("https://example.com/python.png", "Logo 1", width="100px"),
        ImageItem("https://example.com/java.png", "Logo 2", width="100px"),
        ImageItem("https://example.com/ruby.png", "Logo 3", width="100px"),
        ImageItem("https://example.com/js.png", "Logo 4", width="100px")
    ],
    correct_index=0
)
```

### Six Answer Quiz

```python
quiz = QuizTemplate(
    question=TextItem("Which is a planet?"),
    answers=[
        TextItem("Earth"),
        TextItem("Pluto"),
        TextItem("Moon"),
        TextItem("Sun"),
        TextItem("Asteroid Belt"),
        TextItem("ISS")
    ],
    correct_index=0
)
```

## Item Types

### TextItem

```python
TextItem(
    content="Your text here",
    css_class="custom-style"  # optional
)
```

Renders as: `<p class="custom-style">Your text here</p>`

### ImageItem

```python
ImageItem(
    url="https://example.com/image.png",
    alt="Description",
    css_class="img-style",  # optional
    width="300px",           # optional
    height="200px"           # optional
)
```

Renders as: `<img src="..." alt="..." width="300px" height="200px" />`

### VideoItem

```python
VideoItem(
    url="https://example.com/video.mp4",
    thumbnail="https://example.com/thumb.jpg",  # optional
    controls=True,                              # optional
    autoplay=False                              # optional
)
```

Renders as: `<video poster="..." controls><source src="..." /></video>`

### AudioItem

```python
AudioItem(
    url="https://example.com/audio.mp3",
    controls=True,   # optional
    autoplay=False   # optional
)
```

Renders as: `<audio controls><source src="..." /></audio>`

## QuizTemplate Methods

### render(include_solution=False, css_classes=None)

Render quiz as HTML.

```python
# Without solution
html = quiz.render()

# With solution (highlights correct answer)
html = quiz.render(include_solution=True)

# Custom CSS classes
html = quiz.render(css_classes={
    'container': 'my-quiz',
    'question': 'my-question',
    'answers': 'my-answers',
    'answer': 'my-answer'
})
```

### check_answer(user_answer)

Check if answer is correct.

```python
is_correct = quiz.check_answer(1)  # Returns True/False
```

### to_dict(include_solution=False)

Convert to dictionary for storage/transmission.

```python
# For client (no solution)
client_data = quiz.to_dict(include_solution=False)

# For storage (with solution)
storage_data = quiz.to_dict(include_solution=True)
```

### from_dict(data)

Load quiz from dictionary.

```python
quiz = QuizTemplate.from_dict(storage_data)
```

## QuizTemplateRegistry

Manage multiple quizzes:

```python
from templates import QuizTemplateRegistry

registry = QuizTemplateRegistry()

# Register quizzes
registry.register('quiz_001', quiz1)
registry.register('quiz_002', quiz2)

# Retrieve quiz
quiz = registry.get('quiz_001')

# List all IDs
ids = registry.list_ids()

# Remove quiz
registry.remove('quiz_001')

# Count quizzes
count = registry.count()
```

## Security

All HTML output is automatically escaped to prevent XSS attacks:

```python
TextItem("<script>alert('xss')</script>")
# Renders as: &lt;script&gt;alert('xss')&lt;/script&gt;
```

## Serialization Example

```python
# Create quiz
quiz = QuizTemplate(...)

# Save to database
db.save('quiz_001', quiz.to_dict(include_solution=True))

# Load from database
data = db.load('quiz_001')
quiz = QuizTemplate.from_dict(data)

# Send to client (no solution)
client_data = quiz.to_dict(include_solution=False)
socket.emit('quiz', client_data)
```

## Integration with Server

See `server_integration_example.py` for a complete Flask integration with:
- List quizzes: `GET /quiz/list`
- Get HTML: `GET /quiz/<id>/html`
- Get data: `GET /quiz/<id>/data`
- Submit answer: `POST /quiz/<id>/submit`
- Assign to room: `POST /room/<code>/quiz`

## Examples

Run `examples.py` to see all features in action:

```bash
python examples.py
```

Run the integration server:

```bash
python server_integration_example.py
```

Test the API:

```bash
python test_quiz_api.py
```

## Design Principles

1. **Composition over Inheritance**: Items compose into quizzes
2. **Interface-based**: Server works with Item interface, doesn't need to know concrete types
3. **Flexibility**: Easy to add new Item types (e.g., CodeItem, EquationItem)
4. **Security First**: Automatic HTML escaping
5. **Type Safety**: Full type hints for IDE support
6. **Serializable**: Easy storage and transmission

## Extending

Add new item types by inheriting from `Item`:

```python
from templates.items import Item

class CodeItem(Item):
    def __init__(self, code: str, language: str = "python"):
        self.code = code
        self.language = language

    def render(self) -> str:
        from html import escape
        safe_code = escape(self.code)
        return f'<pre><code class="language-{self.language}">{safe_code}</code></pre>'

    def to_dict(self):
        return {'type': 'code', 'code': self.code, 'language': self.language}
```

## License

Part of OpenQuiz Server - see main LICENSE file.
