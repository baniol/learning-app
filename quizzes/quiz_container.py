"""
Quiz container for displaying active quizzes.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal
import quizzes.styles as styles

class QuizContainer(QWidget):
    """Container for displaying the current quiz."""
    
    # Signal to notify when user wants to return to menu
    return_to_menu = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.QUIZ_CONTAINER_BORDER_STYLE)
        
        # Setup layout with zero margins
        self.quiz_layout = QVBoxLayout()
        self.quiz_layout.setContentsMargins(0, 0, 0, 0)
        self.quiz_layout.setSpacing(0) # No spacing between elements
        self.setLayout(self.quiz_layout)
        
        # Quiz state
        self.current_quiz = None
    
    def set_quiz(self, quiz):
        """Set the current quiz and display it."""
        # Clear previous quiz if any
        for i in reversed(range(self.quiz_layout.count())): 
            widget = self.quiz_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Add new quiz
        self.quiz_layout.addWidget(quiz)
        self.current_quiz = quiz
        quiz.generate_new_question() 