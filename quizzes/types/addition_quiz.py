"""
Addition quiz implementation.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
import random
from ..base_quiz import BaseQuiz
from ..components import NavigationBar
from ..styles import (
    DEFAULT_SPACING
)

class AdditionQuiz(BaseQuiz):
    """Quiz for practicing addition problems."""
    
    def __init__(self, parent=None, total_questions=10, show_questions_control=True):
        """Initialize the addition quiz.
        
        Args:
            parent: Parent widget
            total_questions: Number of questions in the quiz
            show_questions_control: Whether to show the questions count control
        """
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
    
    def set_total_questions(self, value):
        """Set the total number of questions."""
        super().set_total_questions(value) 