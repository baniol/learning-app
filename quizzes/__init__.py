"""
Quiz application package.
"""
import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from .multiplication_quiz import MultiplicationQuiz
from .addition_quiz import AdditionQuiz
from .components import VisualAidWidget, NavigationBar, Dot, DotsGroup
from .base_quiz import BaseQuiz
from .styles import *

def create_custom_quiz(
    name,
    number_generator,
    answer_calculator,
    question_formatter=None,
    visual_aid_class=None,
    total_questions=20
):
    """Create a custom quiz with minimal code.
    
    Args:
        name: Name of the quiz to display
        number_generator: Function that takes quiz as argument and sets num1, num2
        answer_calculator: Function that takes quiz as argument and returns the answer
        question_formatter: Function that takes quiz as argument and returns question text
        visual_aid_class: Optional class to use for visual aid (must take num1, num2 as init params)
        total_questions: Default number of questions
        
    Returns:
        A custom quiz class that can be instantiated
    """
    class CustomQuiz(BaseQuiz):
        """Custom quiz generated with factory function."""
        
        def __init__(self, total_questions=total_questions, show_questions_control=True):
            """Initialize the custom quiz.
            
            Args:
                total_questions: Number of questions in the quiz
                show_questions_control: Whether to show the questions count control
            """
            super().__init__(total_questions=total_questions)
            self.quiz_name = name
            
            # Add navigation bar
            self.nav_bar = NavigationBar(self.return_to_menu)
            
            # Add questions control if requested
            if show_questions_control:
                self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                    initial_value=total_questions,
                    callback=self.update_total_questions
                )
            
            # Add visual aid if provided
            if visual_aid_class:
                self.setup_visual_aid(visual_aid_class)
                
            self.layout.insertWidget(0, self.nav_bar)
        
        def setup_visual_aid(self, visual_aid_class):
            """Set up the visual aid for this quiz."""
            # Visual aid container setup
            self.visual_aid_container = QWidget()
            self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.visual_aid_layout = QVBoxLayout()
            self.visual_aid_layout.setContentsMargins(0, 0, 0, 0)
            self.visual_aid_container.setLayout(self.visual_aid_layout)
            
            # Add visual aid toggle checkbox
            self.show_visual_aid_checkbox = self.nav_bar.add_checkbox(
                "Pokaż podpowiedź", True, self.toggle_visual_aid
            )
            
            # Initial visual aid (will be replaced in on_new_question)
            self.visual_aid = visual_aid_class(0, 0)
            self.visual_aid_layout.addWidget(self.visual_aid)
            
            # Add container to main layout
            self.layout.insertWidget(1, self.visual_aid_container)
            
        def toggle_visual_aid(self, state):
            """Toggle the visibility of the visual aid."""
            show_visual_aid = self.show_visual_aid_checkbox.isChecked()
            
            # Show or hide the container
            self.visual_aid_container.setVisible(show_visual_aid)
            
            # When making visible, ensure it gets proper size
            if show_visual_aid:
                # Update the visual aid container with the proper height but don't set a fixed height
                self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            else:
                # When hiding, use Ignored policy to completely remove from layout
                self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
            
            # Force layout updates
            self.layout.activate()
            self.layout.update()
            
            # Force layout updates to parent widgets
            if self.parent():
                self.parent().layout().activate()
                self.parent().layout().update()
                
            # Request an update to the whole window
            self.window().update()
        
        def on_new_question(self):
            """Update the visual aid when a new question is generated."""
            if hasattr(self, 'visual_aid') and hasattr(self, 'visual_aid_container'):
                # Store current visibility state
                was_visible = self.show_visual_aid_checkbox.isChecked()
                
                # Remove old visual aid
                self.visual_aid.setParent(None)
                self.visual_aid.deleteLater()
                
                # Create new visual aid
                self.visual_aid = visual_aid_class(self.num1, self.num2)
                
                # Add to container and restore visibility
                self.visual_aid_layout.addWidget(self.visual_aid)
                
                # Update visibility based on checkbox state
                self.toggle_visual_aid(was_visible)
        
        def generate_numbers(self):
            """Generate numbers for this quiz question."""
            number_generator(self)
            
        def calculate_answer(self):
            """Calculate the answer for the current question."""
            return answer_calculator(self)
            
        def format_question(self):
            """Format the question text."""
            if question_formatter:
                return question_formatter(self)
            # Default format if none provided
            return f"{self.num1} ? {self.num2} = ?"
            
        def format_question_with_answer(self):
            """Format the question with the answer included."""
            if question_formatter:
                # Replace the question mark with the answer
                question = question_formatter(self)
                return question.replace("?", str(self.correct_answer))
            # Default format if none provided
            return f"{self.num1} ? {self.num2} = {self.correct_answer}"
            
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
    
    return CustomQuiz

# Import the custom quizzes
from .custom_quizzes import SmallMultiplicationQuiz, SubtractionQuiz

__all__ = [
    'MultiplicationQuiz', 
    'AdditionQuiz',
    'VisualAidWidget',
    'NavigationBar',
    'Dot',
    'DotsGroup',
    'create_custom_quiz',
    'SmallMultiplicationQuiz',
    'SubtractionQuiz'
] 