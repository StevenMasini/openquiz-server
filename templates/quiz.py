"""
QuizTemplate implementation using Item composition
Supports flexible quiz structures with different content types
"""

from typing import List, Dict, Any, Optional, Type
from html import escape
import json
from pathlib import Path
from .items import Item, item_from_dict


class QuizTemplate:
    """
    Flexible quiz template using Item composition

    A quiz consists of:
    - question: An Item (can be text, image, video, etc.)
    - answers: List of Items
    - correct_index: Index of the correct answer
    - metadata: Optional additional data (points, time_limit, etc.)
    """

    def __init__(
        self,
        question: Item,
        answers: List[Item],
        correct_index: int,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Args:
            question: The question as an Item
            answers: List of answer Items
            correct_index: Index (0-based) of the correct answer
            metadata: Optional dict with points, time_limit, difficulty, etc.
        """
        self.question = question
        self.answers = answers
        self.correct_index = correct_index
        self.metadata = metadata or {}

        # Validate
        if not answers:
            raise ValueError("Quiz must have at least one answer")
        if not (0 <= correct_index < len(answers)):
            raise ValueError(f"correct_index {correct_index} out of range for {len(answers)} answers")

    def render(self, include_solution: bool = False, css_classes: Optional[Dict[str, str]] = None) -> str:
        """
        Render the full quiz as HTML

        Args:
            include_solution: If True, highlights the correct answer
            css_classes: Optional dict with CSS classes for different elements
                        {'container': '...', 'question': '...', 'answers': '...', 'answer': '...'}

        Returns:
            HTML string representing the quiz
        """
        css = css_classes or {}

        container_class = f' class="{escape(css.get("container", "quiz-container"))}"'
        question_class = f' class="{escape(css.get("question", "quiz-question"))}"'
        answers_class = f' class="{escape(css.get("answers", "quiz-answers"))}"'
        answer_class = css.get("answer", "quiz-answer")

        # Start building HTML
        html_parts = [f'<div{container_class}>']

        # Render question
        html_parts.append(f'<div{question_class}>')
        html_parts.append(self.question.render())
        html_parts.append('</div>')

        # Render answers
        html_parts.append(f'<div{answers_class}>')
        for idx, answer in enumerate(self.answers):
            # Add correct/incorrect classes if showing solution
            answer_css = answer_class
            if include_solution:
                if idx == self.correct_index:
                    answer_css += " correct"
                else:
                    answer_css += " incorrect"

            html_parts.append(f'<div class="{escape(answer_css)}" data-answer-index="{idx}">')
            html_parts.append(answer.render())
            html_parts.append('</div>')
        html_parts.append('</div>')

        # Add metadata if present
        if self.metadata:
            html_parts.append('<div class="quiz-metadata" style="display:none;">')
            for key, value in self.metadata.items():
                html_parts.append(f'<span data-{escape(key)}="{escape(str(value))}"></span>')
            html_parts.append('</div>')

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    def check_answer(self, user_answer: int) -> bool:
        """
        Check if the user's answer is correct

        Args:
            user_answer: Index of the user's selected answer

        Returns:
            True if correct, False otherwise
        """
        return user_answer == self.correct_index

    def validate(self) -> bool:
        """Validate quiz structure"""
        try:
            return (
                self.question is not None and
                len(self.answers) > 0 and
                0 <= self.correct_index < len(self.answers)
            )
        except:
            return False

    def to_dict(self, include_solution: bool = False) -> Dict[str, Any]:
        """
        Convert quiz to dictionary for storage/transmission

        Args:
            include_solution: If True, includes correct_index (for storage)
                            If False, omits it (for client transmission)

        Returns:
            Dictionary representation
        """
        result = {
            'question': self.question.to_dict(),
            'answers': [answer.to_dict() for answer in self.answers],
            'metadata': self.metadata
        }

        if include_solution:
            result['correct_index'] = self.correct_index

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuizTemplate':
        """
        Create QuizTemplate from dictionary

        Args:
            data: Dictionary with quiz data

        Returns:
            QuizTemplate instance
        """
        question = item_from_dict(data['question'])
        answers = [item_from_dict(answer_data) for answer_data in data['answers']]
        correct_index = data['correct_index']
        metadata = data.get('metadata', {})

        return cls(question, answers, correct_index, metadata)

    def to_json_file(self, filepath: str, include_solution: bool = True, indent: int = 2) -> None:
        """
        Save QuizTemplate to a JSON file

        Args:
            filepath: Path to the JSON file to write
            include_solution: If True, includes correct_index in the output
            indent: Number of spaces for JSON indentation (default: 2, None for compact)

        Raises:
            IOError: If file cannot be written
        """
        path = Path(filepath)

        # Create parent directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict and write to file
        data = self.to_dict(include_solution=include_solution)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

    @classmethod
    def from_json_file(cls, filepath: str) -> 'QuizTemplate':
        """
        Load QuizTemplate from a JSON file

        Args:
            filepath: Path to the JSON file to read

        Returns:
            QuizTemplate instance

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
            ValueError: If JSON data is invalid for QuizTemplate
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"Quiz template file not found: {filepath}")

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return cls.from_dict(data)


class QuizTemplateRegistry:
    """
    Registry for managing quiz templates
    Useful for storing and retrieving quizzes by ID
    """

    def __init__(self):
        self._templates: Dict[str, QuizTemplate] = {}

    def register(self, quiz_id: str, template: QuizTemplate) -> None:
        """Register a quiz template with an ID"""
        self._templates[quiz_id] = template

    def get(self, quiz_id: str) -> Optional[QuizTemplate]:
        """Retrieve a quiz template by ID"""
        return self._templates.get(quiz_id)

    def list_ids(self) -> List[str]:
        """List all registered quiz IDs"""
        return list(self._templates.keys())

    def remove(self, quiz_id: str) -> bool:
        """Remove a quiz template"""
        if quiz_id in self._templates:
            del self._templates[quiz_id]
            return True
        return False

    def count(self) -> int:
        """Count registered templates"""
        return len(self._templates)
