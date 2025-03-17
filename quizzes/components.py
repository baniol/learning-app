"""
Reusable UI components for the quiz application.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QCheckBox, QSizePolicy
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor
from .styles import (
    BLUE_DOT_COLOR, RED_DOT_COLOR, YELLOW_DOT_COLOR, 
    DOTS_CONTAINER_BORDER_STYLE, FIRST_GROUP_BORDER_STYLE, 
    SECOND_GROUP_BORDER_STYLE, VISUAL_AID_BORDER_STYLE,
    NUMBER_LABEL_STYLE, SHOW_HINT_BUTTON_STYLE,
    EXPLANATION_LABEL_STYLE, DEFAULT_SPACING, DOTS_ROW_SIZE,
    NAV_BAR_BORDER_STYLE, RETURN_BUTTON_STYLE,
    VISUAL_AID_HEIGHT, SCORE_GOOD_COLOR, SCORE_BAD_COLOR,
    SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT, SCORE_BOX_STYLE
)

class NavigationBar(QWidget):
    """Navigation bar with return button and optional controls."""
    def __init__(self, return_callback, parent=None):
        super().__init__(parent)
        self.setStyleSheet(NAV_BAR_BORDER_STYLE)
        self.setFixedHeight(40)  # Fixed height for nav bar
        
        # Create layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)  # No vertical margins
        self.setLayout(self.layout)
        
        # Add return button
        self.return_button = QPushButton("Return to Menu")
        self.return_button.setMinimumSize(150, 30)
        self.return_button.setStyleSheet(RETURN_BUTTON_STYLE)
        self.return_button.clicked.connect(return_callback)
        self.layout.addWidget(self.return_button)
        
        # Add spacer to push other controls to the right
        self.layout.addStretch()
    
    def add_checkbox(self, label, checked=True, callback=None):
        """Add a checkbox to the navigation bar."""
        checkbox = QCheckBox(label)
        checkbox.setChecked(checked)
        if callback:
            checkbox.stateChanged.connect(callback)
        self.layout.addWidget(checkbox)
        return checkbox

class Dot(QWidget):
    """A simple dot widget used for visual representations."""
    def __init__(self, color=RED_DOT_COLOR, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.color = QColor(*color)  # Convert RGB tuple to QColor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(0, 0, 20, 20)
        
    def set_color(self, color):
        """Change the dot's color and update its appearance."""
        self.color = QColor(*color)
        self.update()  # Trigger a repaint

class DotsGroup(QWidget):
    """A group of dots representing a number."""
    def __init__(self, number, color, label_text, parent=None):
        super().__init__(parent)
        self.setStyleSheet(FIRST_GROUP_BORDER_STYLE if color == BLUE_DOT_COLOR else SECOND_GROUP_BORDER_STYLE)
        self.number = number
        self.color = color
        self.dots = []
        self.added_dots = []  # Track dots that were added later
        
        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(DEFAULT_SPACING)
        self.setLayout(self.layout)
        
        # Add label
        self.label = QLabel(label_text)
        self.label.setStyleSheet(NUMBER_LABEL_STYLE)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        # Create dots container
        self.dots_container = QWidget()
        self.dots_container.setStyleSheet(DOTS_CONTAINER_BORDER_STYLE)
        self.dots_layout = QVBoxLayout()
        self.dots_layout.setSpacing(DEFAULT_SPACING)
        self.dots_container.setLayout(self.dots_layout)
        self.layout.addWidget(self.dots_container)
        
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
        """Add new dots with the specified color."""
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
        """Update the label text."""
        self.label.setText(text)
            
    def get_dots(self):
        """Return the list of dots."""
        return self.dots
    
    def clear_added_dots(self):
        """Remove any dots that were added after initialization."""
        for dot in self.added_dots:
            dot.setParent(None)
        self.added_dots = []

class VisualAidWidget(QWidget):
    """Visual aid for addition problems showing dots representation."""
    def __init__(self, num1, num2):
        super().__init__()
        self.setStyleSheet(VISUAL_AID_BORDER_STYLE)
        # Set minimum height instead of fixed height to allow more flexible layout
        self.setMinimumHeight(VISUAL_AID_HEIGHT)
        # Use a policy that works better with layout changes
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.num1 = num1
        self.num2 = num2
        self.complement_shown = False
        
        # Main layout - changed to horizontal
        self.layout = QHBoxLayout()
        self.layout.setSpacing(DEFAULT_SPACING)
        self.setLayout(self.layout)
        
        # Left side container for dots
        self.dots_container = QWidget()
        self.dots_layout = QVBoxLayout()
        self.dots_layout.setSpacing(DEFAULT_SPACING)
        self.dots_container.setLayout(self.dots_layout)
        self.layout.addWidget(self.dots_container, 4)  # Give more space to dots
        
        # Container for the visual representation
        self.visual_container = QWidget()
        self.visual_layout = QHBoxLayout()
        self.visual_layout.setSpacing(DEFAULT_SPACING * 2)  # Double spacing between groups
        self.visual_container.setLayout(self.visual_layout)
        self.dots_layout.addWidget(self.visual_container)
        
        # Create dot groups
        self.first_group = DotsGroup(num1, BLUE_DOT_COLOR, f"{num1}")
        self.second_group = DotsGroup(num2, RED_DOT_COLOR, f"{num2}")
        
        # Add groups to main layout
        self.visual_layout.addWidget(self.first_group)
        self.visual_layout.addWidget(self.second_group)
        
        # Determine which number to complement to 10
        self.larger_number = max(num1, num2)
        self.smaller_number = min(num1, num2)
        self.complement = 10 - self.larger_number if self.larger_number < 10 else 0
        
        # Right side container for controls (button)
        self.controls_container = QWidget()
        self.controls_layout = QVBoxLayout()
        self.controls_layout.setContentsMargins(5, 0, 0, 0)  # Small left margin
        self.controls_container.setLayout(self.controls_layout)
        self.layout.addWidget(self.controls_container, 1)  # Less space for button
        
        # Add complement button if needed
        if self.complement > 0:
            self.add_complement_controls()
    
    def add_complement_controls(self):
        """Add controls for showing the complement to 10."""
        # Add show button
        self.show_button = QPushButton("Podpowiedź")
        self.show_button.setMinimumSize(100, 40)
        self.show_button.setStyleSheet(SHOW_HINT_BUTTON_STYLE)
        self.show_button.clicked.connect(self.show_complement)
        self.controls_layout.addWidget(self.show_button, alignment=Qt.AlignCenter)
    
    def show_complement(self):
        if self.complement <= 0 or self.complement_shown:
            return
            
        # Determine which group has the larger number
        if self.num1 == self.larger_number:
            larger_group = self.first_group
            smaller_group = self.second_group
            larger_number = self.num1
            smaller_number = self.num2
        else:
            larger_group = self.second_group
            smaller_group = self.first_group
            larger_number = self.num2
            smaller_number = self.num1
        
        # Clear any previously added dots
        larger_group.clear_added_dots()
        
        # Get dots from smaller group
        smaller_dots = smaller_group.get_dots()
        
        # Number of dots to move (limited by the smaller number)
        dots_to_move = min(self.complement, len(smaller_dots))
        
        # Hide dots from the smaller group (to simulate moving them)
        for i in range(dots_to_move):
            if i < len(smaller_dots):
                smaller_dots[i].hide()
        
        # Add yellow dots to the larger group to make it 10
        larger_group.add_dots(self.complement, YELLOW_DOT_COLOR)
        
        # Update the labels
        larger_group.update_label(f"{larger_number} + {self.complement} = 10")
        smaller_group.update_label(f"{smaller_number} - {dots_to_move} = {smaller_number - dots_to_move}")
        
        self.complement_shown = True 

class ScoreIndicator(QWidget):
    """A score indicator showing a horizontal bar with green (correct) and red (incorrect) portions."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(SCORE_BOX_WIDTH * 3, SCORE_BOX_HEIGHT)  # Make it wider for better visualization
        self.setStyleSheet(SCORE_BOX_STYLE)
        self.correct = 0
        self.total = 0
        
    def set_score(self, correct, total):
        """Set the score values and update the display."""
        self.correct = correct
        self.total = total
        self.update()  # Trigger repaint
        
    def paintEvent(self, event):
        """Paint the score indicator with proportional green/red bars."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the background/border
        width = self.width() - 2  # Account for border
        height = self.height() - 2
        
        # Start with a blank/empty indicator when no questions answered
        if self.total == 0:
            return
            
        # Calculate proportions
        correct_width = int((self.correct / self.total) * width) if self.total > 0 else 0
        incorrect_width = width - correct_width
        
        # Draw the correct (green) portion
        if correct_width > 0:
            painter.setBrush(QColor(*SCORE_GOOD_COLOR))
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRect(1, 1, correct_width, height))
        
        # Draw the incorrect (red) portion
        if incorrect_width > 0:
            painter.setBrush(QColor(*SCORE_BAD_COLOR))
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRect(1 + correct_width, 1, incorrect_width, height)) 