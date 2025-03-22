"""
Custom quizzes created using the factory function.
"""
import random

# Import create_custom_quiz directly from base module's scope
import sys
import importlib
from pathlib import Path

# Get the quizzes module
quizzes_path = Path(__file__).parent.parent
if str(quizzes_path) not in sys.path:
    sys.path.append(str(quizzes_path))

# Import the module that contains create_custom_quiz
from quizzes.create_quiz_factory import create_custom_quiz

def create_small_multiplication_quiz(total_questions=15):
    """Create a multiplication quiz for numbers 1-5."""
    
    def generate_numbers(quiz):
        """Generate numbers from 2 to 5 for multiplication."""
        quiz.num1 = random.randint(2, 5)
        quiz.num2 = random.randint(2, 5)
    
    def calculate_answer(quiz):
        """Calculate the product of the two numbers."""
        return quiz.num1 * quiz.num2
    
    def format_question(quiz):
        """Format the multiplication question."""
        return f"{quiz.num1} × {quiz.num2} = ?"
    
    # Create the quiz class
    return create_custom_quiz(
        name="Mnożenie małych liczb",
        number_generator=generate_numbers,
        answer_calculator=calculate_answer,
        question_formatter=format_question,
        total_questions=total_questions
    )

def create_subtraction_quiz(total_questions=15):
    """Create a subtraction quiz where we subtract from numbers between 10 and 20."""
    
    def generate_numbers(quiz):
        """Generate numbers where the first is between 10 and 20."""
        quiz.num1 = random.randint(10, 20)  # First number (minuend) between 10 and 20
        quiz.num2 = random.randint(1, 9)    # Second number (subtrahend) between 1 and 9
    
    def calculate_answer(quiz):
        """Calculate the difference."""
        return quiz.num1 - quiz.num2
    
    def format_question(quiz):
        """Format the subtraction question."""
        return f"{quiz.num1} - {quiz.num2} = ?"
    
    # Create the quiz class
    return create_custom_quiz(
        name="Odejmowanie od 10-20",
        number_generator=generate_numbers,
        answer_calculator=calculate_answer,
        question_formatter=format_question,
        total_questions=total_questions
    )

# Create the quiz classes
SmallMultiplicationQuiz = create_small_multiplication_quiz()
SubtractionQuiz = create_subtraction_quiz() 