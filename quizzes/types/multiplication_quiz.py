"""
Multiplication quiz implementation.
"""
import random
from ..base_quiz import BaseQuiz
from ..components import NavigationBar

class MultiplicationQuiz(BaseQuiz):
    """Quiz for practicing multiplication problems."""
    
    def __init__(self, total_questions=20, show_questions_control=True):
        """Initialize the multiplication quiz.
        
        Args:
            total_questions: Number of questions in the quiz
            show_questions_control: Whether to show the questions count control
        """
        super().__init__(total_questions=total_questions)
        
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
                callback=self.update_total_questions
            )
        
        self.layout.insertWidget(0, self.nav_bar)
    
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
        return f"{self.num1} × {self.num2} = {self.correct_answer}" 