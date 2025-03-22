"""
Quiz factory functions for creating custom quizzes.
"""
import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel
from PySide6.QtCore import Qt
from .base_quiz import BaseQuiz
from .components.navigation_bar import NavigationBar
from .debug import log

def create_custom_quiz(
    name,
    number_generator,
    answer_calculator,
    question_formatter=None,
    total_questions=20,
    input_mode=None
):
    """Create a custom quiz with minimal code.
    
    Args:
        name: Name of the quiz to display
        number_generator: Function that takes quiz as argument and sets num1, num2
        answer_calculator: Function that takes quiz as argument and returns the answer
        question_formatter: Function that takes quiz as argument and returns question text
        total_questions: Default number of questions
        input_mode: If provided, fixes the input mode:
                   - True: use input field mode
                   - False: use buttons mode 
                   - "self_assess": use self-assessment mode with reveal button
        
    Returns:
        A custom quiz class that can be instantiated
    """
    class CustomQuiz(BaseQuiz):
        """Custom quiz generated with factory function."""
        
        def __init__(self, parent=None, total_questions=total_questions, show_questions_control=True):
            """Initialize the custom quiz.
            
            Args:
                parent: Parent widget
                total_questions: Number of questions in the quiz
                show_questions_control: Whether to show the questions count control
            """
            super().__init__(
                parent=parent,
                total_questions=total_questions,
                show_questions_control=show_questions_control,
                input_mode=input_mode
            )
            self.quiz_name = name
            
            # Add navigation bar
            self.nav_bar = NavigationBar(self.return_to_menu)
            
            # Add questions control if requested
            if show_questions_control:
                self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                    initial_value=total_questions,
                    callback=self.set_total_questions
                )
            
            # Add input mode toggle only if input mode is not fixed
            if input_mode is None:
                self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
                    checked=False,
                    callback=self.toggle_input_mode
                )
                
            self.main_layout.insertWidget(0, self.nav_bar)
        
        def generate_numbers(self):
            """Generate numbers for this quiz."""
            number_generator(self)
        
        def calculate_answer(self):
            """Calculate the answer for this quiz."""
            return answer_calculator(self)
        
        def format_question(self):
            """Format the question text."""
            if question_formatter:
                return question_formatter(self)
            # Default formatter if none provided
            return f"{self.num1} ? {self.num2}"
        
        def format_question_with_answer(self):
            """Format the question text with the answer included."""
            if question_formatter:
                return f"{question_formatter(self)} = {self.expected_answer}"
            # Default formatter if none provided
            return f"{self.num1} ? {self.num2} = {self.expected_answer}"
        
        def set_total_questions(self, value):
            """Set the total number of questions."""
            # Just calling parent method to ensure type hints are preserved
            super().set_total_questions(value)
            
    return CustomQuiz 