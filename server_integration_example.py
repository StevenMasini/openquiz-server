"""
Example integration of quiz templates with the matchmaking server
Demonstrates how to serve quizzes through Flask endpoints
"""

from flask import Flask, jsonify, request
from templates import TextItem, ImageItem, QuizTemplate, QuizTemplateRegistry

app = Flask(__name__)

# Initialize quiz registry (in production, load from database)
quiz_registry = QuizTemplateRegistry()


def setup_sample_quizzes():
    """Setup some sample quizzes for demonstration"""

    # Basic text quiz
    quiz_registry.register('basic_001', QuizTemplate(
        question=TextItem("What is the capital of France?"),
        answers=[
            TextItem("London"),
            TextItem("Paris"),
            TextItem("Berlin"),
            TextItem("Madrid")
        ],
        correct_index=1,
        metadata={
            'difficulty': 'easy',
            'points': 10,
            'time_limit': 30,
            'category': 'geography'
        }
    ))

    # Image-based quiz
    quiz_registry.register('image_001', QuizTemplate(
        question=ImageItem(
            url="https://example.com/flags/flag.png",
            alt="Country flag",
            width="300px"
        ),
        answers=[
            TextItem("United States"),
            TextItem("France"),
            TextItem("United Kingdom"),
            TextItem("Netherlands")
        ],
        correct_index=2,
        metadata={
            'difficulty': 'medium',
            'points': 15,
            'time_limit': 25,
            'category': 'geography'
        }
    ))

    # Mixed media quiz (text question, image answers)
    quiz_registry.register('mixed_001', QuizTemplate(
        question=TextItem("Which logo represents Python programming language?"),
        answers=[
            ImageItem("https://example.com/logos/python.png", "Logo 1", width="120px"),
            ImageItem("https://example.com/logos/java.png", "Logo 2", width="120px"),
            ImageItem("https://example.com/logos/ruby.png", "Logo 3", width="120px"),
            ImageItem("https://example.com/logos/javascript.png", "Logo 4", width="120px")
        ],
        correct_index=0,
        metadata={
            'difficulty': 'easy',
            'points': 10,
            'time_limit': 20,
            'category': 'programming'
        }
    ))

    # Six-answer quiz
    quiz_registry.register('six_answers_001', QuizTemplate(
        question=TextItem("Which of the following is a planet in our solar system?"),
        answers=[
            TextItem("Earth"),
            TextItem("Pluto"),
            TextItem("Moon"),
            TextItem("Sun"),
            TextItem("Asteroid Belt"),
            TextItem("International Space Station")
        ],
        correct_index=0,
        metadata={
            'difficulty': 'medium',
            'points': 15,
            'time_limit': 30,
            'category': 'astronomy'
        }
    ))


@app.route('/quiz/list', methods=['GET'])
def list_quizzes():
    """
    List all available quizzes

    Response:
    {
        "quizzes": ["basic_001", "image_001", ...],
        "total": 4
    }
    """
    quiz_ids = quiz_registry.list_ids()
    return jsonify({
        'quizzes': quiz_ids,
        'total': len(quiz_ids)
    }), 200


@app.route('/quiz/<quiz_id>/html', methods=['GET'])
def get_quiz_html(quiz_id: str):
    """
    Get quiz rendered as HTML (for web clients)

    Query params:
    - show_solution: true/false (default: false)

    Response:
    {
        "quiz_id": "basic_001",
        "html": "<div>...</div>",
        "metadata": {...}
    }
    """
    quiz = quiz_registry.get(quiz_id)

    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    show_solution = request.args.get('show_solution', 'false').lower() == 'true'

    return jsonify({
        'quiz_id': quiz_id,
        'html': quiz.render(include_solution=show_solution),
        'metadata': quiz.metadata
    }), 200


@app.route('/quiz/<quiz_id>/data', methods=['GET'])
def get_quiz_data(quiz_id: str):
    """
    Get quiz as structured data (for mobile/custom clients)

    Response:
    {
        "quiz_id": "basic_001",
        "question": {...},
        "answers": [...],
        "metadata": {...}
    }
    """
    quiz = quiz_registry.get(quiz_id)

    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    # Don't include solution when sending to client
    data = quiz.to_dict(include_solution=False)
    data['quiz_id'] = quiz_id

    return jsonify(data), 200


@app.route('/quiz/<quiz_id>/submit', methods=['POST'])
def submit_answer(quiz_id: str):
    """
    Submit an answer for a quiz

    Request body:
    {
        "answer": 1,  // Index of selected answer
        "player_id": "player123"  // Optional player identifier
    }

    Response:
    {
        "quiz_id": "basic_001",
        "correct": true,
        "points_earned": 10
    }
    """
    quiz = quiz_registry.get(quiz_id)

    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    data = request.get_json()
    if not data or 'answer' not in data:
        return jsonify({'error': 'Answer is required'}), 400

    try:
        user_answer = int(data['answer'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Answer must be an integer'}), 400

    # Check if answer is valid
    if not (0 <= user_answer < len(quiz.answers)):
        return jsonify({'error': f'Answer must be between 0 and {len(quiz.answers) - 1}'}), 400

    # Check answer
    is_correct = quiz.check_answer(user_answer)

    # Calculate points
    points_earned = quiz.metadata.get('points', 0) if is_correct else 0

    return jsonify({
        'quiz_id': quiz_id,
        'correct': is_correct,
        'points_earned': points_earned,
        'correct_answer': quiz.correct_index if not is_correct else None  # Show correct answer if wrong
    }), 200


@app.route('/room/<room_code>/quiz', methods=['POST'])
def assign_quiz_to_room(room_code: str):
    """
    Assign a quiz to a game room (integration with matchmaking)

    Request body:
    {
        "quiz_id": "basic_001"
    }

    Response:
    {
        "room_code": "123456",
        "quiz_id": "basic_001",
        "quiz_html": "<div>...</div>"
    }
    """
    quiz_id = request.get_json().get('quiz_id')

    if not quiz_id:
        return jsonify({'error': 'quiz_id is required'}), 400

    quiz = quiz_registry.get(quiz_id)

    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    # Here you would integrate with your room storage
    # For now, just return the quiz data

    return jsonify({
        'room_code': room_code,
        'quiz_id': quiz_id,
        'quiz_html': quiz.render(),
        'quiz_data': quiz.to_dict(include_solution=False),
        'metadata': quiz.metadata
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'quizzes_loaded': quiz_registry.count()
    }), 200


if __name__ == '__main__':
    print("Setting up sample quizzes...")
    setup_sample_quizzes()

    print(f"Loaded {quiz_registry.count()} quizzes")
    print("\nAvailable endpoints:")
    print("  GET  /quiz/list - List all quizzes")
    print("  GET  /quiz/<id>/html - Get quiz as HTML")
    print("  GET  /quiz/<id>/data - Get quiz as structured data")
    print("  POST /quiz/<id>/submit - Submit an answer")
    print("  POST /room/<code>/quiz - Assign quiz to room")
    print()

    app.run(debug=True, host='0.0.0.0', port=4231)
