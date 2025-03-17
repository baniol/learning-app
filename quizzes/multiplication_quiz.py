"""
Multiplication quiz implementation.
"""
from .base_quiz import BaseQuiz
from .components import NavigationBar

class MultiplicationQuiz(BaseQuiz):
    """Quiz for practicing multiplication problems."""
    
    def __init__(self):
        """Initialize the multiplication quiz."""
        super().__init__()
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        self.layout.insertWidget(0, self.nav_bar)
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.parent().parent().show_menu()
    
    def calculate_answer(self):
        """Calculate the product of the two numbers."""
        return self.num1 * self.num2

    def format_question(self):
        """Format the multiplication question."""
        return f"{self.num1} × {self.num2} = ?"

    def format_question_with_answer(self):
        """Format the multiplication question with the answer."""
        return f"{self.num1} × {self.num2} = {self.correct_answer}" 