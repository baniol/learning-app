"""
Quiz application package.
"""
import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel
from .base_quiz import BaseQuiz
from .styles import *

# Import and expose the factory function
from .create_quiz_factory import create_custom_quiz

# Import quiz types from the types subpackage
from .types import (
    AdditionQuiz,
    MultiplicationQuiz,
    SmallMultiplicationQuiz,
    SubtractionQuiz
)

__all__ = [
    'MultiplicationQuiz', 
    'AdditionQuiz',
    'create_custom_quiz',
    'SmallMultiplicationQuiz',
    'SubtractionQuiz'
] 