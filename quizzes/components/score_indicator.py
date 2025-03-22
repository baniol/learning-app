"""
Score indicator component for quiz application.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor
from ..styles import (
    SCORE_GOOD_COLOR, SCORE_BAD_COLOR,
    SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT, SCORE_BOX_STYLE
)

class ScoreIndicator(QWidget):
    """Visual indicator for quiz score showing a colored box with score percentage."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.correct = 0
        self.total = 0
        self.answered = 0  # Track answered questions separately
        self.setFixedSize(SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT)
        self.setStyleSheet(SCORE_BOX_STYLE)
    
    def set_score(self, correct, total, current_question=None):
        """Set the score values and update the display.
        
        Args:
            correct: Number of correct answers
            total: Total number of questions in the quiz
            current_question: Current question number (1-based, None means not started)
        """
        self.correct = correct
        self.total = total
        
        # Update answered questions count - current_question represents the question being asked or just answered
        if current_question is not None:
            # Set answered to the current question number since that's the question that was just answered
            self.answered = current_question
        else:
            self.answered = 0
            
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Draw the score indicator with green for correct and red for incorrect answers."""
        if self.answered == 0:
            # No questions answered yet
            return
        
        # For answered questions, use the count of correct answers and incorrect answers
        # rather than a ratio based on total questions
        
        # Calculate correct and incorrect counts based on answered questions only
        incorrect = self.answered - self.correct
        
        # For the first correct answer, ensure it shows as 100% green
        if self.answered == 1 and self.correct == 1:
            # Show 100% green for first correct answer
            painter = QPainter(self)
            painter.fillRect(QRect(0, 0, self.width(), self.height()), QColor(*SCORE_GOOD_COLOR))
            painter.end()
            return
        elif self.answered == 1 and self.correct == 0:
            # Show 100% red for first incorrect answer
            painter = QPainter(self)
            painter.fillRect(QRect(0, 0, self.width(), self.height()), QColor(*SCORE_BAD_COLOR))
            painter.end()
            return
        
        # For multiple questions, calculate proportions
        correct_ratio = self.correct / self.answered if self.answered > 0 else 0
        incorrect_ratio = incorrect / self.answered if self.answered > 0 else 0
        
        # Draw green part for correct answers and red for incorrect
        green_width = int(self.width() * correct_ratio)
        red_width = int(self.width() * incorrect_ratio)
        
        painter = QPainter(self)
        
        # Draw green portion (correct answers)
        if green_width > 0:
            painter.fillRect(QRect(0, 0, green_width, self.height()), QColor(*SCORE_GOOD_COLOR))
        
        # Draw red portion (incorrect answers)
        if red_width > 0:
            painter.fillRect(QRect(green_width, 0, red_width, self.height()), QColor(*SCORE_BAD_COLOR))
        
        painter.end() 