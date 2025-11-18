"""
Quiz Template System
Provides a flexible, compositional approach to defining quiz questions and answers
"""

from .items import Item, TextItem, ImageItem, VideoItem, AudioItem
from .quiz import QuizTemplate, QuizTemplateRegistry

__all__ = [
    'Item',
    'TextItem',
    'ImageItem',
    'VideoItem',
    'AudioItem',
    'QuizTemplate',
    'QuizTemplateRegistry'
]
