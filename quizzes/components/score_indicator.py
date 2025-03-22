"""
Score indicator for quiz application.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QRect
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
        self.setFixedSize(SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT)
        self.setStyleSheet(SCORE_BOX_STYLE)
    
    def set_score(self, correct, total, current_question=None):
        """Set the score values and update the display.
        
        Args:
            correct: Number of correct answers
            total: Total number of questions in the quiz
            current_question: Current question number (ignored in this implementation)
        """
        self.correct = correct
        self.total = total
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Draw the score indicator with appropriate color."""
        if self.total == 0:
            # No score to display yet
            return
        
        # Calculate percentage of correct answers
        percentage = self.correct / self.total
        
        # Interpolate between red and green based on percentage
        if percentage >= 0.8:  # 80% or better is good (green)
            color = QColor(*SCORE_GOOD_COLOR)
        elif percentage <= 0.4:  # 40% or worse is bad (red)
            color = QColor(*SCORE_BAD_COLOR)
        else:
            # Linear interpolation between red and green
            r = int(SCORE_BAD_COLOR[0] * (1 - percentage) + SCORE_GOOD_COLOR[0] * percentage)
            g = int(SCORE_BAD_COLOR[1] * (1 - percentage) + SCORE_GOOD_COLOR[1] * percentage)
            b = int(SCORE_BAD_COLOR[2] * (1 - percentage) + SCORE_GOOD_COLOR[2] * percentage)
            color = QColor(r, g, b)
        
        # Calculate width based on percentage
        width = int(self.width() * percentage)
        
        # Draw the background (already handled by stylesheet)
        
        # Draw the colored portion
        painter = QPainter(self)
        painter.fillRect(QRect(0, 0, width, self.height()), color)
        painter.end() 