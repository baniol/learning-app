"""
Visual elements for quiz visualizations.

This module provides low-level visual elements like dots and dot groups
that are used to build visual aids for quizzes.
"""
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor

from ..new_components.base_component import BaseComponent
from ..styles import (
    BLUE_DOT_COLOR, RED_DOT_COLOR, YELLOW_DOT_COLOR, 
    DOTS_CONTAINER_BORDER_STYLE, FIRST_GROUP_BORDER_STYLE, 
    SECOND_GROUP_BORDER_STYLE, NUMBER_LABEL_STYLE,
    DEFAULT_SPACING, DOTS_ROW_SIZE
)


class Dot(BaseComponent):
    """A simple dot widget used for visual representations."""
    
    def __init__(self, color=RED_DOT_COLOR, parent=None):
        """Initialize a dot with the specified color.
        
        Args:
            color: RGB tuple for the dot color
            parent: Parent widget
        """
        super().__init__(parent=parent)
        self.setFixedSize(20, 20)
        self.color = QColor(*color)  # Convert RGB tuple to QColor

    def paintEvent(self, event):
        """Paint the dot."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(0, 0, 20, 20)
        
    def set_color(self, color):
        """Change the dot's color and update its appearance.
        
        Args:
            color: RGB tuple for the new color
        """
        self.color = QColor(*color)
        self.update()  # Trigger a repaint


class DotsGroup(BaseComponent):
    """A group of dots representing a number."""
    
    def __init__(self, number, color, label_text, parent=None):
        """Initialize a group of dots with a label.
        
        Args:
            number: The number of dots to display
            color: RGB tuple for the dot color
            label_text: Text to display as the label
            parent: Parent widget
        """
        # Set style based on color
        style = FIRST_GROUP_BORDER_STYLE if color == BLUE_DOT_COLOR else SECOND_GROUP_BORDER_STYLE
        
        super().__init__(
            parent=parent,
            style=style
        )
        
        self.number = number
        self.color = color
        self.dots = []
        self.added_dots = []  # Track dots that were added later
        
        # Create layout
        self.main_layout = self.create_layout(
            orientation='vertical',
            spacing=DEFAULT_SPACING
        )
        
        # Add label
        self.label = QLabel(label_text)
        self.label.setStyleSheet(NUMBER_LABEL_STYLE)
        self.label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label)
        
        # Create dots container
        self.dots_container = QWidget()
        self.dots_container.setStyleSheet(DOTS_CONTAINER_BORDER_STYLE)
        self.dots_layout = QVBoxLayout()
        self.dots_layout.setSpacing(DEFAULT_SPACING)
        self.dots_container.setLayout(self.dots_layout)
        self.main_layout.addWidget(self.dots_container)
        
        # Create dots
        self.create_dots()
        
    def create_dots(self):
        """Create dots arranged in rows."""
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignCenter)
        self.dots_layout.addLayout(row)
        
        for i in range(self.number):
            if i > 0 and i % DOTS_ROW_SIZE == 0:
                row = QHBoxLayout()
                row.setAlignment(Qt.AlignCenter)
                self.dots_layout.addLayout(row)
            
            dot = Dot(self.color)
            self.dots.append(dot)
            row.addWidget(dot)
    
    def add_dots(self, count, color):
        """Add new dots with the specified color.
        
        Args:
            count: Number of dots to add
            color: RGB tuple for the dot color
        """
        # Find the last row or create a new one
        if self.dots_layout.count() == 0:
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignCenter)
            self.dots_layout.addLayout(row)
        else:
            last_row = self.dots_layout.itemAt(self.dots_layout.count() - 1).layout()
            if last_row.count() >= DOTS_ROW_SIZE:
                # Create a new row if the last one is full
                row = QHBoxLayout()
                row.setAlignment(Qt.AlignCenter)
                self.dots_layout.addLayout(row)
            else:
                row = last_row
        
        # Add new dots
        for i in range(count):
            # Check if we need a new row
            if row.count() >= DOTS_ROW_SIZE:
                row = QHBoxLayout()
                row.setAlignment(Qt.AlignCenter)
                self.dots_layout.addLayout(row)
            
            dot = Dot(color)
            self.added_dots.append(dot)
            row.addWidget(dot)
    
    def update_label(self, text):
        """Update the label text.
        
        Args:
            text: New label text
        """
        self.label.setText(text)
            
    def get_dots(self):
        """Return the list of dots.
        
        Returns:
            List of Dot widgets
        """
        return self.dots
    
    def clear_added_dots(self):
        """Remove any dots that were added after initialization."""
        for dot in self.added_dots:
            dot.setParent(None)
        self.added_dots = [] 