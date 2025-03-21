"""
Quiz type implementations.
This subpackage contains all the specific quiz implementations.
"""
from .addition_quiz import AdditionQuiz
from .multiplication_quiz import MultiplicationQuiz
from .custom_quizzes import SmallMultiplicationQuiz, SubtractionQuiz

__all__ = [
    'AdditionQuiz',
    'MultiplicationQuiz',
    'SmallMultiplicationQuiz',
    'SubtractionQuiz'
] 