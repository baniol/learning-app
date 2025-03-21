"""
Visual aid components for quiz application.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter

from ..styles import (
    BLUE_DOT_COLOR, RED_DOT_COLOR, YELLOW_DOT_COLOR, 
    VISUAL_AID_BORDER_STYLE, DEFAULT_SPACING, VISUAL_AID_HEIGHT,
    SHOW_HINT_BUTTON_STYLE, NUMBER_LABEL_STYLE
)

# Import directly from components_py.py file instead of components package
from ..components_py import Dot, DotsGroup

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

class SubtractionVisualAidWidget(QWidget):
    """Visual aid for subtraction problems showing dots representation in a two-column layout."""
    def __init__(self, num1, num2):
        super().__init__()
        self.setStyleSheet(VISUAL_AID_BORDER_STYLE)
        self.setMinimumHeight(VISUAL_AID_HEIGHT)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.num1 = num1  # The minuend (starting number)
        self.num2 = num2  # The subtrahend (number to subtract)
        self.solution_shown = False
        
        # Main layout - horizontal
        self.layout = QHBoxLayout()
        self.layout.setSpacing(DEFAULT_SPACING)
        self.setLayout(self.layout)
        
        # Left side container for dots
        self.dots_container = QWidget()
        self.dots_layout = QVBoxLayout()
        self.dots_layout.setSpacing(DEFAULT_SPACING)
        self.dots_container.setLayout(self.dots_layout)
        self.layout.addWidget(self.dots_container, 4)  # Give more space to dots
        
        # Add title label
        if num1 == 0:
            # Handle initialization with zeros (happens during startup)
            self.title_label = QLabel("Pomoce wizualne wczytują się...")
        else:
            self.title_label = QLabel(f"{num1} - {num2} = ?")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.dots_layout.addWidget(self.title_label)
        
        # Container for the visual representation - horizontal layout like addition
        self.visual_container = QWidget()
        self.visual_layout = QHBoxLayout()
        self.visual_layout.setSpacing(DEFAULT_SPACING * 2)  # Double spacing between groups
        self.visual_container.setLayout(self.visual_layout)
        self.dots_layout.addWidget(self.visual_container)
        
        # Create dot groups
        self.first_group = DotsGroup(num1, BLUE_DOT_COLOR, f"Mamy {num1}")
        self.second_group = DotsGroup(num2, RED_DOT_COLOR, f"Odejmujemy {num2}")
        
        # Add groups to main layout
        self.visual_layout.addWidget(self.first_group)
        self.visual_layout.addWidget(self.second_group)
        
        # Result group (initially hidden)
        self.result_group = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_group.setLayout(self.result_layout)
        self.result_group.hide()
        self.dots_layout.addWidget(self.result_group)
        
        # Result label
        self.result_label = QLabel(f"Zostaje {num1 - num2}")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_layout.addWidget(self.result_label)
        
        # Create container for result dots
        self.dots_result_container = QWidget()
        self.dots_result_layout = QVBoxLayout()
        self.dots_result_container.setLayout(self.dots_result_layout)
        
        # Add label for result dots
        self.dots_result_label = QLabel("Wynik:")
        self.dots_result_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.dots_result_label.setAlignment(Qt.AlignCenter)
        self.dots_result_layout.addWidget(self.dots_result_label)
        
        # Grid for result dots
        self.dots_result_grid = QVBoxLayout()
        self.dots_result_layout.addLayout(self.dots_result_grid)
        
        # Add result dots container to result layout (but don't show yet)
        self.result_layout.addWidget(self.dots_result_container)
        
        # Right side container for controls (button)
        self.controls_container = QWidget()
        self.controls_layout = QVBoxLayout()
        self.controls_layout.setContentsMargins(5, 0, 0, 0)  # Small left margin
        self.controls_container.setLayout(self.controls_layout)
        self.layout.addWidget(self.controls_container, 1)  # Less space for button
        
        # Add show button if not showing zeros
        if num1 > 0 and num2 > 0:
            self.show_button = QPushButton("Pokaż rozwiązanie")
            self.show_button.setMinimumSize(120, 40)
            self.show_button.setStyleSheet(SHOW_HINT_BUTTON_STYLE)
            self.show_button.clicked.connect(self.show_solution)
            self.controls_layout.addWidget(self.show_button, alignment=Qt.AlignCenter)
    
    def show_solution(self):
        """Show the subtraction solution."""
        if self.solution_shown:
            return
        
        # Calculate result
        result_value = self.num1 - self.num2
        
        # Clear any existing content in the grid
        while self.dots_result_grid.count():
            item = self.dots_result_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create row for result dots
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignCenter)
        self.dots_result_grid.addLayout(row)
        
        # Add yellow dots for the result
        for i in range(result_value):
            if i > 0 and i % 5 == 0:  # Create new row every 5 dots
                row = QHBoxLayout()
                row.setAlignment(Qt.AlignCenter)
                self.dots_result_grid.addLayout(row)
            
            dot = Dot(YELLOW_DOT_COLOR)
            row.addWidget(dot)
        
        # Update title label to show the solution
        self.title_label.setText(f"{self.num1} - {self.num2} = {result_value}")
        
        # Update group labels
        self.first_group.update_label(f"Mieliśmy {self.num1}")
        self.second_group.update_label(f"Odjęliśmy {self.num2}")
        
        # Show the result group
        self.result_group.show()
        
        self.solution_shown = True
        
        # Disable button
        self.show_button.setEnabled(False)
        self.show_button.setText("Rozwiązanie pokazane") 