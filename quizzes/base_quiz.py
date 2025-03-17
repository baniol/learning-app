"""
Base quiz class that provides common functionality for all quizzes.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
import random
from .styles import (
    QUESTION_LABEL_STYLE, QUESTION_CORRECT_STYLE, QUESTION_INCORRECT_STYLE,
    FEEDBACK_LABEL_STYLE, FEEDBACK_CORRECT_STYLE, FEEDBACK_INCORRECT_STYLE,
    ANSWER_BUTTON_STYLE, NEXT_BUTTON_STYLE, MAIN_BORDER_STYLE,
    DEFAULT_SPACING, BUTTON_SPACING
)

class BaseQuiz(QWidget):
    """Base class for all quizzes with common UI and functionality."""
    
    def __init__(self):
        """Initialize the quiz with basic UI components."""
        super().__init__()
        self.setStyleSheet(MAIN_BORDER_STYLE)
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 0, 10, 10)  # Left, Top, Right, Bottom
        self.layout.setSpacing(DEFAULT_SPACING)
        self.setLayout(self.layout)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet(QUESTION_LABEL_STYLE)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.question_label)
        
        # Answer buttons container - horizontal layout
        self.answers_widget = QWidget()
        self.answers_layout = QHBoxLayout()
        self.answers_layout.setSpacing(BUTTON_SPACING)
        self.answers_widget.setLayout(self.answers_layout)
        self.layout.addWidget(self.answers_widget)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet(FEEDBACK_LABEL_STYLE)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)
        
        # Next question button
        self.next_button = QPushButton("Next Question")
        self.next_button.setMinimumSize(200, 50)
        self.next_button.setStyleSheet(NEXT_BUTTON_STYLE)
        self.next_button.clicked.connect(self.generate_new_question)
        self.next_button.hide()
        self.layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
        
        # Initialize quiz state
        self.num1 = 0
        self.num2 = 0
        self.correct_answer = 0

    def generate_new_question(self):
        """Generate a new question and update the UI."""
        # Clear previous answer buttons
        self.clear_answer_buttons()
        
        # Generate new question
        self.generate_numbers()
        self.correct_answer = self.calculate_answer()
        
        # Update question label with default style
        self.question_label.setText(self.format_question())
        self.question_label.setStyleSheet(QUESTION_LABEL_STYLE)
        
        # Generate answer options
        options = self.generate_answer_options()
        
        # Create new answer buttons
        self.create_answer_buttons(options)
        
        # Hide feedback and next button
        self.feedback_label.setText("")
        self.next_button.hide()
        
        # Additional setup for specific quiz types
        self.on_new_question()
    
    def generate_numbers(self):
        """Generate random numbers for the question. Override in subclasses if needed."""
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
    
    def on_new_question(self):
        """Hook for subclasses to perform additional setup after generating a new question."""
        pass
    
    def clear_answer_buttons(self):
        """Clear all answer buttons from the layout."""
        for i in reversed(range(self.answers_layout.count())): 
            self.answers_layout.itemAt(i).widget().setParent(None)
    
    def generate_answer_options(self):
        """Generate answer options including the correct answer and distractors."""
        options = [self.correct_answer]
        while len(options) < 4:
            wrong_answer = self.correct_answer + random.randint(-5, 5)
            if wrong_answer != self.correct_answer and wrong_answer not in options and wrong_answer > 0:
                options.append(wrong_answer)
        
        random.shuffle(options)
        return options
    
    def create_answer_buttons(self, options):
        """Create buttons for each answer option."""
        for option in options:
            button = QPushButton(str(option))
            button.setMinimumSize(100, 80)
            button.setStyleSheet(ANSWER_BUTTON_STYLE)
            button.clicked.connect(lambda checked, ans=option: self.check_answer(ans))
            self.answers_layout.addWidget(button)

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct and update the UI accordingly."""
        # Disable all answer buttons
        for i in range(self.answers_layout.count()):
            button = self.answers_layout.itemAt(i).widget()
            button.setEnabled(False)
        
        if selected_answer == self.correct_answer:
            self.show_correct_feedback()
        else:
            self.show_incorrect_feedback()
        
        self.next_button.show()
    
    def show_correct_feedback(self):
        """Show feedback for a correct answer."""
        self.feedback_label.setText("Correct! Well done!")
        self.feedback_label.setStyleSheet(FEEDBACK_CORRECT_STYLE)
        self.question_label.setText(self.format_question_with_answer())
        self.question_label.setStyleSheet(QUESTION_CORRECT_STYLE)
    
    def show_incorrect_feedback(self):
        """Show feedback for an incorrect answer."""
        self.feedback_label.setText(f"Wrong! The correct answer was {self.correct_answer}")
        self.feedback_label.setStyleSheet(FEEDBACK_INCORRECT_STYLE)
        self.question_label.setText(self.format_question_with_answer())
        self.question_label.setStyleSheet(QUESTION_INCORRECT_STYLE)

    def calculate_answer(self):
        """Calculate the correct answer based on the generated numbers."""
        raise NotImplementedError("Subclasses must implement calculate_answer")

    def format_question(self):
        """Format the question text."""
        raise NotImplementedError("Subclasses must implement format_question")

    def format_question_with_answer(self):
        """Format the question text with the answer included."""
        raise NotImplementedError("Subclasses must implement format_question_with_answer") 