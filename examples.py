"""
Examples demonstrating the quiz template system
Shows different quiz types and usage patterns
"""

from templates import TextItem, ImageItem, VideoItem, AudioItem, QuizTemplate, QuizTemplateRegistry


def example_basic_text_quiz():
    """Basic multiple choice with text only"""
    quiz = QuizTemplate(
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
            'time_limit': 30
        }
    )

    print("=== Basic Text Quiz ===")
    print(quiz.render())
    print("\n" + "="*50 + "\n")

    # Check answers
    print("Answer 0 correct?", quiz.check_answer(0))  # False
    print("Answer 1 correct?", quiz.check_answer(1))  # True
    print("\n" + "="*50 + "\n")


def example_image_question_quiz():
    """Quiz with image as question"""
    quiz = QuizTemplate(
        question=ImageItem(
            url="https://example.com/flags/france.png",
            alt="Flag image",
            width="300px"
        ),
        answers=[
            TextItem("France"),
            TextItem("Italy"),
            TextItem("Netherlands"),
            TextItem("Russia")
        ],
        correct_index=0,
        metadata={
            'difficulty': 'medium',
            'points': 15,
            'time_limit': 20
        }
    )

    print("=== Image Question Quiz ===")
    print(quiz.render())
    print("\n" + "="*50 + "\n")


def example_mixed_media_quiz():
    """Quiz with text question and image answers"""
    quiz = QuizTemplate(
        question=TextItem("Which logo belongs to Python?"),
        answers=[
            ImageItem("https://example.com/logos/python.png", "Python logo", width="100px"),
            ImageItem("https://example.com/logos/java.png", "Java logo", width="100px"),
            ImageItem("https://example.com/logos/ruby.png", "Ruby logo", width="100px"),
            ImageItem("https://example.com/logos/javascript.png", "JavaScript logo", width="100px")
        ],
        correct_index=0,
        metadata={
            'difficulty': 'easy',
            'points': 10,
            'category': 'programming'
        }
    )

    print("=== Mixed Media Quiz ===")
    print(quiz.render())
    print("\n" + "="*50 + "\n")


def example_audio_quiz():
    """Quiz with audio question"""
    quiz = QuizTemplate(
        question=AudioItem(
            url="https://example.com/audio/mystery-sound.mp3",
            controls=True
        ),
        answers=[
            TextItem("Dog barking"),
            TextItem("Cat meowing"),
            TextItem("Bird chirping"),
            TextItem("Door creaking")
        ],
        correct_index=2,
        metadata={
            'difficulty': 'hard',
            'points': 20,
            'category': 'audio-identification'
        }
    )

    print("=== Audio Quiz ===")
    print(quiz.render())
    print("\n" + "="*50 + "\n")


def example_video_quiz():
    """Quiz with video question"""
    quiz = QuizTemplate(
        question=VideoItem(
            url="https://example.com/videos/scene.mp4",
            thumbnail="https://example.com/thumbnails/scene.jpg",
            controls=True,
            autoplay=False
        ),
        answers=[
            TextItem("New York"),
            TextItem("Los Angeles"),
            TextItem("Chicago"),
            TextItem("San Francisco")
        ],
        correct_index=3,
        metadata={
            'difficulty': 'medium',
            'points': 15,
            'category': 'geography'
        }
    )

    print("=== Video Quiz ===")
    print(quiz.render())
    print("\n" + "="*50 + "\n")


def example_six_answer_quiz():
    """Quiz with 6 answers instead of 4"""
    quiz = QuizTemplate(
        question=TextItem("Which of these are programming languages?"),
        answers=[
            TextItem("Python"),
            TextItem("JavaScript"),
            TextItem("HTML"),
            TextItem("CSS"),
            TextItem("Java"),
            TextItem("SQL")
        ],
        correct_index=0,  # Could be 0, 1, 4, or 5 depending on interpretation
        metadata={
            'difficulty': 'medium',
            'points': 15,
            'note': 'This demonstrates 6 answers instead of 4'
        }
    )

    print("=== Six Answer Quiz ===")
    print(quiz.render())
    print("\n" + "="*50 + "\n")


def example_with_solution():
    """Show quiz with solution highlighted"""
    quiz = QuizTemplate(
        question=TextItem("What is 2 + 2?"),
        answers=[
            TextItem("3"),
            TextItem("4"),
            TextItem("5"),
            TextItem("6")
        ],
        correct_index=1
    )

    print("=== Quiz Without Solution ===")
    print(quiz.render(include_solution=False))
    print("\n")

    print("=== Quiz With Solution ===")
    print(quiz.render(include_solution=True))
    print("\n" + "="*50 + "\n")


def example_serialization():
    """Demonstrate saving and loading quizzes"""
    # Create a quiz
    original_quiz = QuizTemplate(
        question=TextItem("What is Python?"),
        answers=[
            TextItem("A snake"),
            TextItem("A programming language"),
            TextItem("A type of coffee"),
            TextItem("A movie")
        ],
        correct_index=1,
        metadata={'difficulty': 'easy'}
    )

    print("=== Serialization Example ===")

    # Convert to dict (for client - no solution)
    client_data = original_quiz.to_dict(include_solution=False)
    print("Client data (no solution):")
    print(client_data)
    print()

    # Convert to dict (for storage - with solution)
    storage_data = original_quiz.to_dict(include_solution=True)
    print("Storage data (with solution):")
    print(storage_data)
    print()

    # Reconstruct from storage
    loaded_quiz = QuizTemplate.from_dict(storage_data)
    print("Loaded quiz renders correctly:")
    print(loaded_quiz.render())
    print("\n" + "="*50 + "\n")


def example_json_file_serialization():
    """Demonstrate saving and loading quizzes from JSON files"""
    import os
    import tempfile

    # Create a quiz
    original_quiz = QuizTemplate(
        question=TextItem("What is the speed of light?"),
        answers=[
            TextItem("299,792,458 m/s"),
            TextItem("300,000,000 m/s"),
            TextItem("186,282 miles/s"),
            TextItem("670,616,629 mph")
        ],
        correct_index=0,
        metadata={
            'difficulty': 'hard',
            'points': 25,
            'category': 'physics',
            'time_limit': 45
        }
    )

    print("=== JSON File Serialization Example ===")

    # Create a temporary directory for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save to JSON file (with solution for storage)
        storage_path = os.path.join(temp_dir, 'quizzes', 'physics_001.json')
        original_quiz.to_json_file(storage_path, include_solution=True)
        print(f"Quiz saved to: {storage_path}")
        print()

        # Read and display the JSON file content
        with open(storage_path, 'r') as f:
            print("JSON file content:")
            print(f.read())
        print()

        # Load the quiz back from file
        loaded_quiz = QuizTemplate.from_json_file(storage_path)
        print("Quiz loaded successfully!")
        print(f"Question: {loaded_quiz.question.content}")
        print(f"Number of answers: {len(loaded_quiz.answers)}")
        print(f"Correct answer: {loaded_quiz.answers[loaded_quiz.correct_index].content}")
        print(f"Metadata: {loaded_quiz.metadata}")
        print()

        # Save without solution (for client distribution)
        client_path = os.path.join(temp_dir, 'client_quiz.json')
        original_quiz.to_json_file(client_path, include_solution=False)
        print(f"Client version saved to: {client_path}")
        with open(client_path, 'r') as f:
            print("Client JSON (note: no correct_index):")
            print(f.read())

    print("\n" + "="*50 + "\n")


def example_registry():
    """Demonstrate using the registry"""
    registry = QuizTemplateRegistry()

    # Register multiple quizzes
    registry.register('quiz_001', QuizTemplate(
        question=TextItem("Question 1?"),
        answers=[TextItem("A"), TextItem("B"), TextItem("C"), TextItem("D")],
        correct_index=0
    ))

    registry.register('quiz_002', QuizTemplate(
        question=ImageItem("https://example.com/image.png", "Image"),
        answers=[TextItem("A"), TextItem("B"), TextItem("C"), TextItem("D")],
        correct_index=1
    ))

    print("=== Registry Example ===")
    print(f"Total quizzes: {registry.count()}")
    print(f"Quiz IDs: {registry.list_ids()}")
    print()

    # Retrieve and use a quiz
    quiz = registry.get('quiz_001')
    if quiz:
        print("Retrieved quiz_001:")
        print(quiz.render())
    print("\n" + "="*50 + "\n")


def example_custom_css():
    """Demonstrate custom CSS classes"""
    quiz = QuizTemplate(
        question=TextItem("Styled question?", css_class="custom-question-style"),
        answers=[
            TextItem("Answer 1", css_class="custom-answer-style"),
            TextItem("Answer 2", css_class="custom-answer-style"),
            TextItem("Answer 3", css_class="custom-answer-style"),
            TextItem("Answer 4", css_class="custom-answer-style")
        ],
        correct_index=0
    )

    print("=== Custom CSS Example ===")
    print(quiz.render(css_classes={
        'container': 'my-quiz-container',
        'question': 'my-question-section',
        'answers': 'my-answers-section',
        'answer': 'my-answer-item'
    }))
    print("\n" + "="*50 + "\n")


if __name__ == '__main__':
    print("\n" + "="*50)
    print("QUIZ TEMPLATE SYSTEM EXAMPLES")
    print("="*50 + "\n")

    example_basic_text_quiz()
    example_image_question_quiz()
    example_mixed_media_quiz()
    example_audio_quiz()
    example_video_quiz()
    example_six_answer_quiz()
    example_with_solution()
    example_serialization()
    example_json_file_serialization()
    example_registry()
    example_custom_css()

    print("All examples completed!")
