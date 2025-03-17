from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from .base_quiz import BaseQuiz
import random

class Dot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.color = QColor(255, 0, 0)  # Red by default

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(0, 0, 20, 20)

class VisualAidWidget(QWidget):
    def __init__(self, num1, num2):
        super().__init__()
        self.setStyleSheet("QWidget { border: 2px solid red; }")  # Main widget border
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)  # Add spacing between elements
        self.setLayout(self.layout)
        
        # Container for the visual representation
        self.visual_container = QWidget()
        self.visual_container.setStyleSheet("QWidget { border: 2px solid blue; }")  # Container border
        self.visual_layout = QHBoxLayout()
        self.visual_layout.setSpacing(40)  # Add spacing between number groups
        self.visual_container.setLayout(self.visual_layout)
        self.layout.addWidget(self.visual_container)
        
        # First number group
        self.first_group = QWidget()
        self.first_group.setStyleSheet("QWidget { border: 2px solid green; }")  # First group border
        first_layout = QVBoxLayout()
        first_layout.setSpacing(10)  # Add spacing between elements
        self.first_group.setLayout(first_layout)
        
        # First number label
        first_label = QLabel(f"First number: {num1}")
        first_label.setStyleSheet("font-size: 16px;")
        first_label.setAlignment(Qt.AlignCenter)  # Center the label
        first_layout.addWidget(first_label)
        
        # First number dots container
        self.first_dots_container = QWidget()
        self.first_dots_container.setStyleSheet("QWidget { border: 2px solid purple; }")  # Dots container border
        self.first_dots_layout = QVBoxLayout()
        self.first_dots_layout.setSpacing(10)  # Add spacing between rows
        self.first_dots_container.setLayout(self.first_dots_layout)
        first_layout.addWidget(self.first_dots_container)
        
        # Create first number dots in rows of 5
        self.first_dots = []
        first_row = QHBoxLayout()
        first_row.setAlignment(Qt.AlignCenter)  # Center the dots
        self.first_dots_layout.addLayout(first_row)
        
        for i in range(num1):
            if i > 0 and i % 5 == 0:
                first_row = QHBoxLayout()
                first_row.setAlignment(Qt.AlignCenter)  # Center the dots
                self.first_dots_layout.addLayout(first_row)
            
            dot = Dot()
            dot.color = QColor(0, 0, 255)  # Blue
            self.first_dots.append(dot)
            first_row.addWidget(dot)
        
        # Second number group
        self.second_group = QWidget()
        self.second_group.setStyleSheet("QWidget { border: 2px solid orange; }")  # Second group border
        second_layout = QVBoxLayout()
        second_layout.setSpacing(10)  # Add spacing between elements
        self.second_group.setLayout(second_layout)
        
        # Second number label
        second_label = QLabel(f"Second number: {num2}")
        second_label.setStyleSheet("font-size: 16px;")
        second_label.setAlignment(Qt.AlignCenter)  # Center the label
        second_layout.addWidget(second_label)
        
        # Second number dots container
        self.second_dots_container = QWidget()
        self.second_dots_container.setStyleSheet("QWidget { border: 2px solid purple; }")  # Dots container border
        self.second_dots_layout = QVBoxLayout()
        self.second_dots_layout.setSpacing(10)  # Add spacing between rows
        self.second_dots_container.setLayout(self.second_dots_layout)
        second_layout.addWidget(self.second_dots_container)
        
        # Create second number dots in rows of 5
        self.second_dots = []
        second_row = QHBoxLayout()
        second_row.setAlignment(Qt.AlignCenter)  # Center the dots
        self.second_dots_layout.addLayout(second_row)
        
        for i in range(num2):
            if i > 0 and i % 5 == 0:
                second_row = QHBoxLayout()
                second_row.setAlignment(Qt.AlignCenter)  # Center the dots
                self.second_dots_layout.addLayout(second_row)
            
            dot = Dot()
            dot.color = QColor(255, 0, 0)  # Red
            self.second_dots.append(dot)
            second_row.addWidget(dot)
        
        # Add groups to main layout
        self.visual_layout.addWidget(self.first_group)
        self.visual_layout.addWidget(self.second_group)
        
        # Determine which number to complement to (the larger one)
        self.target_number = max(num1, num2)
        self.source_number = min(num1, num2)
        self.complement = 10 - self.target_number if self.target_number < 10 else 0
        
        if self.complement > 0:
            # Add show button
            show_button = QPushButton("Show how to make 10")
            show_button.setMinimumSize(200, 40)  # Set minimum size instead of fixed
            # Add distinct styling
            show_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 2px solid #388E3C;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:pressed {
                    background-color: #1B5E20;
                }
            """)
            show_button.clicked.connect(self.show_complement)
            self.layout.addWidget(show_button, alignment=Qt.AlignCenter)
        
        # Store the numbers for complement calculation
        self.num1 = num1
        self.num2 = num2
        self.complement_shown = False

    def show_complement(self):
        if self.complement <= 0 or self.complement_shown:
            return
            
        # Determine which group to move dots from and to
        if self.num1 == self.source_number:
            source_dots = self.first_dots
            source_layout = self.first_dots_layout
            target_dots = self.second_dots
            target_layout = self.second_dots_layout
        else:
            source_dots = self.second_dots
            source_layout = self.second_dots_layout
            target_dots = self.first_dots
            target_layout = self.first_dots_layout
            
        # Move complement number of dots from source group to target group
        dots_to_move = min(self.complement, len(source_dots))
        for _ in range(dots_to_move):
            dot = source_dots.pop(0)  # Take from the beginning
            # Change color to yellow
            dot.color = QColor(255, 255, 0)
            # Move to target group
            source_layout.removeWidget(dot)
            # Add to the appropriate row in target group
            row_index = len(target_dots) // 5
            if row_index >= target_layout.count():
                new_row = QHBoxLayout()
                new_row.setAlignment(Qt.AlignCenter)
                target_layout.addLayout(new_row)
            row = target_layout.itemAt(row_index).layout()
            row.addWidget(dot)
            target_dots.append(dot)

        self.complement_shown = True

    def update_numbers(self, num1, num2):
        # Clear existing dots
        for dot in self.first_dots + self.second_dots:
            dot.setParent(None)
        
        # Create new dots
        self.first_dots = []
        self.second_dots = []
        
        # First number group
        self.first_group = QWidget()
        self.first_group.setStyleSheet("QWidget { border: 2px solid green; }")  # First group border
        first_layout = QVBoxLayout()
        first_layout.setSpacing(10)  # Add spacing between elements
        self.first_group.setLayout(first_layout)
        
        # First number label
        first_label = QLabel(f"First number: {num1}")
        first_label.setStyleSheet("font-size: 16px;")
        first_label.setAlignment(Qt.AlignCenter)  # Center the label
        first_layout.addWidget(first_label)
        
        # First number dots container
        self.first_dots_container = QWidget()
        self.first_dots_container.setStyleSheet("QWidget { border: 2px solid purple; }")  # Dots container border
        self.first_dots_layout = QVBoxLayout()
        self.first_dots_layout.setSpacing(10)  # Add spacing between rows
        self.first_dots_container.setLayout(self.first_dots_layout)
        first_layout.addWidget(self.first_dots_container)
        
        # Create first number dots in rows of 5
        first_row = QHBoxLayout()
        first_row.setAlignment(Qt.AlignCenter)  # Center the dots
        self.first_dots_layout.addLayout(first_row)
        
        for i in range(num1):
            if i > 0 and i % 5 == 0:
                first_row = QHBoxLayout()
                first_row.setAlignment(Qt.AlignCenter)  # Center the dots
                self.first_dots_layout.addLayout(first_row)
            
            dot = Dot()
            dot.color = QColor(0, 0, 255)  # Blue
            self.first_dots.append(dot)
            first_row.addWidget(dot)
        
        # Second number group
        self.second_group = QWidget()
        self.second_group.setStyleSheet("QWidget { border: 2px solid orange; }")  # Second group border
        second_layout = QVBoxLayout()
        second_layout.setSpacing(10)  # Add spacing between elements
        self.second_group.setLayout(second_layout)
        
        # Second number label
        second_label = QLabel(f"Second number: {num2}")
        second_label.setStyleSheet("font-size: 16px;")
        second_label.setAlignment(Qt.AlignCenter)  # Center the label
        second_layout.addWidget(second_label)
        
        # Second number dots container
        self.second_dots_container = QWidget()
        self.second_dots_container.setStyleSheet("QWidget { border: 2px solid purple; }")  # Dots container border
        self.second_dots_layout = QVBoxLayout()
        self.second_dots_layout.setSpacing(10)  # Add spacing between rows
        self.second_dots_container.setLayout(self.second_dots_layout)
        second_layout.addWidget(self.second_dots_container)
        
        # Create second number dots in rows of 5
        second_row = QHBoxLayout()
        second_row.setAlignment(Qt.AlignCenter)  # Center the dots
        self.second_dots_layout.addLayout(second_row)
        
        for i in range(num2):
            if i > 0 and i % 5 == 0:
                second_row = QHBoxLayout()
                second_row.setAlignment(Qt.AlignCenter)  # Center the dots
                self.second_dots_layout.addLayout(second_row)
            
            dot = Dot()
            dot.color = QColor(255, 0, 0)  # Red
            self.second_dots.append(dot)
            second_row.addWidget(dot)
        
        # Add groups to main layout
        self.visual_layout.addWidget(self.first_group)
        self.visual_layout.addWidget(self.second_group)
        
        # Determine which number to complement to (the larger one)
        self.target_number = max(num1, num2)
        self.source_number = min(num1, num2)
        self.complement = 10 - self.target_number if self.target_number < 10 else 0
        
        if self.complement > 0:
            # Add show button
            show_button = QPushButton("Show how to make 10")
            show_button.setMinimumSize(200, 40)  # Set minimum size instead of fixed
            # Add distinct styling
            show_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 2px solid #388E3C;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:pressed {
                    background-color: #1B5E20;
                }
            """)
            show_button.clicked.connect(self.show_complement)
            self.layout.addWidget(show_button, alignment=Qt.AlignCenter)
            
            # Add explanation label
            self.explanation_label = QLabel()
            self.explanation_label.setStyleSheet("font-size: 16px; color: purple;")
            self.explanation_label.setAlignment(Qt.AlignCenter)  # Center the explanation
            self.layout.addWidget(self.explanation_label)
        
        # Store the numbers for complement calculation
        self.num1 = num1
        self.num2 = num2
        self.complement_shown = False

class AdditionQuiz(BaseQuiz):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { border: 2px solid black; }")  # Main quiz border
        
        # Set absolute minimal top padding
        self.layout.setContentsMargins(10, 0, 10, 10)  # Left, Top, Right, Bottom
        self.layout.setSpacing(5)  # Minimal spacing between elements
        
        # Create navigation bar with minimal height
        self.nav_bar = QWidget()
        self.nav_bar.setStyleSheet("QWidget { border: 2px solid yellow; }")  # Nav bar border
        self.nav_bar.setFixedHeight(40)  # Set fixed height for nav bar
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setContentsMargins(5, 0, 5, 0)  # No vertical margins
        self.nav_bar.setLayout(self.nav_layout)
        
        # Add return to menu button with reduced height
        self.return_button = QPushButton("Return to Menu")
        self.return_button.setMinimumSize(150, 30)  # Reduced height
        self.return_button.clicked.connect(self.return_to_menu)
        # Add styling to the return button
        self.return_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                border: 1px solid #ba000d;
            }
            QPushButton:hover {
                background-color: #ba000d;
            }
        """)
        self.nav_layout.addWidget(self.return_button)
        
        # Add spacer to push checkbox to the right
        self.nav_layout.addStretch()
        
        # Move checkbox to nav bar
        self.show_visual_aid_checkbox = QCheckBox("Show dots helper")
        self.show_visual_aid_checkbox.setChecked(True)
        self.show_visual_aid_checkbox.stateChanged.connect(self.toggle_visual_aid)
        self.nav_layout.addWidget(self.show_visual_aid_checkbox)
        
        # Add nav bar to main layout
        self.layout.insertWidget(0, self.nav_bar)
        
        # Add visual aid widget after nav bar
        self.visual_aid = VisualAidWidget(0, 0)
        self.layout.insertWidget(1, self.visual_aid)

    def return_to_menu(self):
        # This will be handled by the main window
        self.parent().parent().show_menu()

    def toggle_visual_aid(self, state):
        self.visual_aid.setVisible(self.show_visual_aid_checkbox.isChecked())
        if self.show_visual_aid_checkbox.isChecked():
            self.visual_aid.updateGeometry()
            self.visual_aid.update()
            self.layout.update()

    def calculate_answer(self):
        return self.num1 + self.num2

    def format_question(self):
        return f"{self.num1} + {self.num2} = ?"

    def format_question_with_answer(self):
        return f"{self.num1} + {self.num2} = {self.correct_answer}"

    def generate_new_question(self):
        # Clear previous answer buttons
        for i in reversed(range(self.answers_layout.count())): 
            self.answers_layout.itemAt(i).widget().setParent(None)
        
        # Generate new question where sum is 10 or greater
        while True:
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
            self.correct_answer = self.calculate_answer()
            if self.correct_answer >= 10:
                break
        
        # Update question label with default style
        self.question_label.setText(self.format_question())
        self.question_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # Store current visibility state
        was_visible = self.visual_aid.isVisible()
        
        # Update visual aid
        self.visual_aid.deleteLater()
        self.visual_aid = VisualAidWidget(self.num1, self.num2)
        self.layout.insertWidget(1, self.visual_aid)
        
        # Restore visibility state
        self.visual_aid.setVisible(was_visible)
        
        # Generate answer options
        options = [self.correct_answer]
        while len(options) < 4:
            wrong_answer = self.correct_answer + random.randint(-5, 5)
            if wrong_answer != self.correct_answer and wrong_answer not in options:
                options.append(wrong_answer)
        
        random.shuffle(options)
        
        # Create new answer buttons with improved styling
        for option in options:
            button = QPushButton(str(option))
            button.setMinimumSize(100, 80)  # Larger, more square buttons
            # Add distinct styling
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4a86e8;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 10px;
                    border: 2px solid #2d5bb9;
                }
                QPushButton:hover {
                    background-color: #2d5bb9;
                }
                QPushButton:pressed {
                    background-color: #1c3a75;
                }
            """)
            button.clicked.connect(lambda checked, ans=option: self.check_answer(ans))
            self.answers_layout.addWidget(button)
        
        # Hide feedback and next button
        self.feedback_label.setText("")
        self.next_button.hide() 