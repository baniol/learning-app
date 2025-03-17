"""
Multiplication quiz implementation.
"""
from .base_quiz import BaseQuiz
from .components import NavigationBar

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
        
        # Add spinbox for number of questions if enabled
        if show_questions_control:
            self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                initial_value=total_questions,
                callback=self.update_total_questions
            )
        
        self.layout.insertWidget(0, self.nav_bar)
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.parent().parent().show_menu()
    
    def update_total_questions(self, value):
        """Update the total number of questions for the quiz."""
        self.total_questions = value
        # Update the progress bar range
        self.progress_bar.setRange(0, value)
        # Update the label
        self.progress_label.setText(f"Pytanie {self.current_question}/{self.total_questions}")
        
        # If we're already past the new total, show results
        if self.current_question > self.total_questions and not self.quiz_completed:
            self.show_results()
    
    def calculate_answer(self):
        """Calculate the product of the two numbers."""
        return self.num1 * self.num2

    def format_question(self):
        """Format the multiplication question."""
        return f"{self.num1} × {self.num2} = ?"

    def format_question_with_answer(self):
        """Format the multiplication question with the answer."""
        return f"{self.num1} × {self.num2} = {self.correct_answer}" 