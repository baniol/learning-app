"""
Custom quizzes created using the factory function.
"""
import random
from .components import VisualAidWidget
from . import create_custom_quiz

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
        visual_aid_class=None,  # No visual aid for multiplication
        total_questions=total_questions
    )

def create_subtraction_quiz(total_questions=15):
    """Create a subtraction quiz where the result is always positive."""
    
    def generate_numbers(quiz):
        """Generate numbers where the first is greater than the second."""
        quiz.num1 = random.randint(10, 20)
        quiz.num2 = random.randint(1, quiz.num1 - 1)  # Ensure positive result
    
    def calculate_answer(quiz):
        """Calculate the difference."""
        return quiz.num1 - quiz.num2
    
    def format_question(quiz):
        """Format the subtraction question."""
        return f"{quiz.num1} - {quiz.num2} = ?"
    
    # Create the quiz class
    return create_custom_quiz(
        name="Odejmowanie",
        number_generator=generate_numbers,
        answer_calculator=calculate_answer,
        question_formatter=format_question,
        visual_aid_class=VisualAidWidget,  # Use the standard visual aid
        total_questions=total_questions
    )

# Create the quiz classes
SmallMultiplicationQuiz = create_small_multiplication_quiz()
SubtractionQuiz = create_subtraction_quiz() 