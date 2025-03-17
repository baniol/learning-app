from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
import random
from PySide6.QtCore import Qt

class BaseQuiz(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Set minimal margins for the main layout
        self.layout.setContentsMargins(10, 0, 10, 10)  # Left, Top, Right, Bottom
        self.layout.setSpacing(10)  # Reduce spacing between widgets
        self.setLayout(self.layout)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.question_label)
        
        # Answer buttons container - changed to horizontal layout
        self.answers_widget = QWidget()
        self.answers_layout = QHBoxLayout()  # Changed from QVBoxLayout to QHBoxLayout
        self.answers_layout.setSpacing(15)  # Add spacing between buttons
        self.answers_widget.setLayout(self.answers_layout)
        self.layout.addWidget(self.answers_widget)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.feedback_label)
        
        # Next question button
        self.next_button = QPushButton("Next Question")
        self.next_button.setMinimumSize(200, 50)
        # Add distinct styling
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                border: 2px solid #F57C00;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)
        self.next_button.clicked.connect(self.generate_new_question)
        self.next_button.hide()
        self.layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

    def generate_new_question(self):
        # Clear previous answer buttons
        for i in reversed(range(self.answers_layout.count())): 
            self.answers_layout.itemAt(i).widget().setParent(None)
        
        # Generate new question
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.correct_answer = self.calculate_answer()
        
        # Update question label with default style
        self.question_label.setText(self.format_question())
        self.question_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
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

    def check_answer(self, selected_answer):
        # Disable all answer buttons
        for i in range(self.answers_layout.count()):
            button = self.answers_layout.itemAt(i).widget()
            button.setEnabled(False)
        
        if selected_answer == self.correct_answer:
            self.feedback_label.setText("Correct! Well done!")
            self.feedback_label.setStyleSheet("font-size: 18px; color: green;")
            self.question_label.setText(self.format_question_with_answer())
            self.question_label.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")
        else:
            self.feedback_label.setText(f"Wrong! The correct answer was {self.correct_answer}")
            self.feedback_label.setStyleSheet("font-size: 18px; color: red;")
            self.question_label.setText(self.format_question_with_answer())
            self.question_label.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
        
        self.next_button.show()

    def calculate_answer(self):
        raise NotImplementedError("Subclasses must implement calculate_answer")

    def format_question(self):
        raise NotImplementedError("Subclasses must implement format_question")

    def format_question_with_answer(self):
        raise NotImplementedError("Subclasses must implement format_question_with_answer") 