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
        
        def __init__(self, parent=None, total_questions=total_questions, show_visual_aid=True, show_questions_control=True):
            """Initialize the custom quiz.
            
            Args:
                parent: Parent widget
                total_questions: Number of questions in the quiz
                show_visual_aid: Whether to show visual aids
                show_questions_control: Whether to show the questions count control
            """
            super().__init__(
                parent=parent,
                total_questions=total_questions,
                show_visual_aid=show_visual_aid,
                show_questions_control=show_questions_control
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
            
            # Add visual aid if provided
            if visual_aid_class:
                self.setup_visual_aid(visual_aid_class, show_visual_aid)
                
            self.main_layout.insertWidget(0, self.nav_bar)
        
        def setup_visual_aid(self, visual_aid_class, initial_visible=True):
            """Set up the visual aid for this quiz."""
            # Visual aid container setup
            self.visual_aid_container = QWidget()
            self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.visual_aid_layout = QVBoxLayout()
            self.visual_aid_layout.setContentsMargins(0, 0, 0, 0)
            self.visual_aid_container.setLayout(self.visual_aid_layout)
            
            # Add visual aid toggle checkbox
            self.show_visual_aid_checkbox = self.nav_bar.add_checkbox(
                "Pokaż podpowiedź", initial_visible, self.toggle_visual_aid
            )
            
            # Store the visual aid class for later use
            self.visual_aid_class = visual_aid_class
            
            # We'll create a placeholder visual aid with zeros
            # The actual visual aid will be created in on_new_question after
            # the first question is generated
            try:
                self.visual_aid = visual_aid_class(0, 0)
                self.visual_aid_layout.addWidget(self.visual_aid)
            except Exception as e:
                log("QuizFactory", f"Error creating initial visual aid: {e}")
                # Create a placeholder widget if the visual aid creation fails
                placeholder = QLabel("Pomoce wizualne wczytają się przy pierwszym pytaniu")
                placeholder.setAlignment(Qt.AlignCenter)
                self.visual_aid = placeholder
                self.visual_aid_layout.addWidget(placeholder)
            
            # Add container to main layout
            self.main_layout.insertWidget(1, self.visual_aid_container)
            
            # Set initial visibility
            self.toggle_visual_aid(initial_visible)
        
        def toggle_visual_aid(self, state):
            """Toggle the visibility of the visual aid."""
            if not hasattr(self, 'visual_aid_container') or not hasattr(self, 'show_visual_aid_checkbox'):
                return
                
            show_visual_aid = state if isinstance(state, bool) else self.show_visual_aid_checkbox.isChecked()
            
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
            self.main_layout.activate()
            self.main_layout.update()
            
            # Force layout updates to parent widgets
            if self.parent():
                self.parent().layout().activate()
                self.parent().layout().update()
                
            # Request an update to the whole window
            self.window().update()
        
        def on_new_question(self):
            """Update the visual aid when a new question is generated."""
            if hasattr(self, 'visual_aid') and hasattr(self, 'visual_aid_container') and hasattr(self, 'visual_aid_class'):
                try:
                    # Store current visibility state
                    was_visible = self.show_visual_aid_checkbox.isChecked()
                    
                    # Remove old visual aid
                    self.visual_aid.setParent(None)
                    self.visual_aid.deleteLater()
                    
                    # Create new visual aid with proper error handling
                    try:
                        self.visual_aid = self.visual_aid_class(self.num1, self.num2)
                        self.visual_aid_layout.addWidget(self.visual_aid)
                    except Exception as e:
                        log("QuizFactory", f"Error creating visual aid: {e}")
                        # Create an error message widget if visual aid creation fails
                        error_widget = QLabel(f"Błąd pomocy wizualnej: {self.num1}, {self.num2}")
                        error_widget.setAlignment(Qt.AlignCenter)
                        self.visual_aid = error_widget
                        self.visual_aid_layout.addWidget(error_widget)
                    
                    # Update visibility based on checkbox state
                    self.toggle_visual_aid(was_visible)
                except Exception as e:
                    log("QuizFactory", f"Error in on_new_question: {str(e)}")
        
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
                return question.replace("?", str(self.expected_answer))
            # Default format if none provided
            return f"{self.num1} ? {self.num2} = {self.expected_answer}"
            
        def set_total_questions(self, value):
            """Set the total number of questions in the quiz."""
            self.total_questions = value
    
    return CustomQuiz 