"""
Consolidated quiz type implementations.
This module contains all quiz implementations in a single file for simplicity.
"""
import random
from ..base_quiz import BaseQuiz
from ..components import NavigationBar
from ..create_quiz_factory import create_custom_quiz

class AdditionQuiz(BaseQuiz):
    """Quiz for practicing addition problems."""
    
    def __init__(self, parent=None, total_questions=10, show_questions_control=True):
        """Initialize the addition quiz."""
        super().__init__(
            parent=parent,
            total_questions=total_questions,
            show_questions_control=show_questions_control
        )
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        
        # Add input mode toggle
        self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
            checked=False,
            callback=self.toggle_input_mode
        )
        
        # Add spinbox for number of questions if enabled
        if show_questions_control:
            self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                initial_value=total_questions,
                callback=self.set_total_questions
            )
        
        self.main_layout.insertWidget(0, self.nav_bar)
    
    def generate_numbers(self):
        """Generate numbers where the sum is 10 or greater."""
        while True:
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
            if self.num1 + self.num2 >= 10:
                break
    
    def calculate_answer(self):
        """Calculate the result of the addition."""
        return self.num1 + self.num2
    
    def format_question(self):
        """Format the addition question."""
        return f"{self.num1} + {self.num2} = ?"
    
    def format_question_with_answer(self):
        """Format the addition question with the answer included."""
        return f"{self.num1} + {self.num2} = {self.expected_answer}"


class MultiplicationQuiz(BaseQuiz):
    """Quiz for practicing multiplication problems."""
    
    def __init__(self, parent=None, total_questions=20, show_questions_control=True):
        """Initialize the multiplication quiz."""
        super().__init__(
            parent=parent,
            total_questions=total_questions,
            show_questions_control=show_questions_control
        )
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        
        # Add input mode toggle
        self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
            checked=False,
            callback=self.toggle_input_mode
        )
        
        # Add spinbox for number of questions if enabled
        if show_questions_control:
            self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                initial_value=total_questions,
                callback=self.set_total_questions
            )
        
        self.main_layout.insertWidget(0, self.nav_bar)
    
    def generate_numbers(self):
        """Generate numbers from 2 to 5 for multiplication, avoiding multiplying by 1."""
        self.num1 = random.randint(2, 5)
        self.num2 = random.randint(2, 5)
    
    def calculate_answer(self):
        """Calculate the product of the two numbers."""
        return self.num1 * self.num2

    def format_question(self):
        """Format the multiplication question."""
        return f"{self.num1} × {self.num2} = ?"

    def format_question_with_answer(self):
        """Format the multiplication question with the answer."""
        return f"{self.num1} × {self.num2} = {self.expected_answer}"


# Factory-created quizzes

def create_small_multiplication_quiz():
    """Create a small multiplication quiz with numbers 2-5."""
    
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
        total_questions=15
    )

def create_subtraction_quiz():
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
        total_questions=15
    )

# Create the quiz classes
SmallMultiplicationQuiz = create_small_multiplication_quiz()
SubtractionQuiz = create_subtraction_quiz() 