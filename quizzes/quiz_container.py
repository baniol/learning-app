"""
Quiz container for displaying active quizzes.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from .new_components.base_component import BaseComponent
from .styles import QUIZ_CONTAINER_BORDER_STYLE

class QuizContainer(BaseComponent):
    """Container for displaying the current quiz.
    
    This container manages the currently active quiz and handles
    cleanup when switching between quizzes.
    """
    
    # Signal to notify when user wants to return to menu
    return_to_menu = Signal()
    
    def __init__(self, parent=None):
        """Initialize the quiz container.
        
        Args:
            parent: Parent widget
        """
        super().__init__(
            parent=parent,
            style=QUIZ_CONTAINER_BORDER_STYLE
        )
        
        # Setup layout with zero margins
        self.quiz_layout = self.create_layout(
            orientation='vertical',
            margins=(0, 0, 0, 0),
            spacing=0
        )
        
        # Quiz state
        self.current_quiz = None
    
    def set_quiz(self, quiz):
        """Set the current quiz and display it.
        
        Args:
            quiz: The quiz instance to display
        """
        # Clean up previous quiz
        self._clear_current_quiz()
        
        # Add new quiz
        self.quiz_layout.addWidget(quiz)
        self.current_quiz = quiz
        
        # No need to call anything here - the quiz is already initialized
        # and next_question was already called during its initialization
    
    def _clear_current_quiz(self):
        """Clear the current quiz from the container."""
        if self.current_quiz:
            self.current_quiz.setParent(None)
            self.current_quiz = None
        else:
            # Remove any widgets from the layout
            for i in reversed(range(self.quiz_layout.count())): 
                widget = self.quiz_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None) 