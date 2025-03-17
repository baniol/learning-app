"""
Template for creating new quizzes.
Copy this file and modify it to create a new quiz type.
"""
from .base_quiz import BaseQuiz
from .components import NavigationBar

class NewQuiz(BaseQuiz):
    """Template for a new quiz type."""
    
    def __init__(self):
        """Initialize the quiz."""
        super().__init__()
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        self.layout.insertWidget(0, self.nav_bar)
        
        # Add any additional UI components here
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.parent().parent().show_menu()
    
    def generate_numbers(self):
        """Generate numbers for the quiz.
        Override this method to customize number generation.
        """
        # Default implementation from BaseQuiz
        super().generate_numbers()
    
    def on_new_question(self):
        """Perform additional setup when a new question is generated.
        Override this method to add custom behavior.
        """
        pass
    
    def calculate_answer(self):
        """Calculate the correct answer based on the generated numbers."""
        # Example: Addition
        return self.num1 + self.num2
    
    def format_question(self):
        """Format the question text."""
        # Example: Addition
        return f"{self.num1} + {self.num2} = ?"
    
    def format_question_with_answer(self):
        """Format the question text with the answer included."""
        # Example: Addition
        return f"{self.num1} + {self.num2} = {self.correct_answer}" 