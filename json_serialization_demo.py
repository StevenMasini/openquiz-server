#!/usr/bin/env python3
"""
Simple demonstration of QuizTemplate JSON serialization
"""

from templates import TextItem, ImageItem, QuizTemplate

# Create a quiz
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

# Save to JSON file (with solution for storage)
quiz.to_json_file('data/quizzes/geography_001.json', include_solution=True)
print("✓ Quiz saved with solution to: data/quizzes/geography_001.json")

# Save client version (without solution)
quiz.to_json_file('data/client/quiz.json', include_solution=False)
print("✓ Client version saved to: data/client/quiz.json")

# Load quiz from file
loaded_quiz = QuizTemplate.from_json_file('data/quizzes/geography_001.json')
print(f"✓ Quiz loaded: {loaded_quiz.question.content}")
print(f"  Correct answer: {loaded_quiz.answers[loaded_quiz.correct_index].content}")

# Create a quiz with mixed media
media_quiz = QuizTemplate(
    question=ImageItem(
        url="https://example.com/flags/france.png",
        alt="Which country's flag is this?",
        width="400px"
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
        'category': 'flags'
    }
)

# Save with compact formatting (no indentation)
media_quiz.to_json_file('data/quizzes/compact_quiz.json', include_solution=True, indent=None)
print("✓ Compact quiz saved to: data/quizzes/compact_quiz.json")

print("\nAll done! Check the data/quizzes directory for the generated JSON files.")
