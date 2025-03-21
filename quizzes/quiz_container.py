"""
Quiz container for displaying active quizzes.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal
import random
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
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet(styles.QUESTION_LABEL_STYLE)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.quiz_layout.addWidget(self.question_label)
        
        # Answer buttons container
        self.answers_widget = QWidget()
        self.answers_widget.setStyleSheet(styles.ANSWERS_CONTAINER_BORDER_STYLE)
        self.answers_layout = QVBoxLayout()
        self.answers_layout.setSpacing(styles.ANSWERS_LAYOUT_SPACING)
        self.answers_widget.setLayout(self.answers_layout)
        self.quiz_layout.addWidget(self.answers_widget)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet(styles.FEEDBACK_LABEL_STYLE)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.quiz_layout.addWidget(self.feedback_label)
        
        # Next question button
        self.next_button = QPushButton("Next Question")
        self.next_button.setMinimumSize(*styles.ANSWER_BUTTON_SIZE)
        self.next_button.clicked.connect(self.generate_new_question)
        self.next_button.hide()
        self.quiz_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
        
        # Quiz state
        self.num1 = 0
        self.num2 = 0
        self.correct_answer = 0
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
    
    def generate_new_question(self):
        """Generate a new basic question (used for built-in quiz types)."""
        # Clear previous answer buttons
        for i in reversed(range(self.answers_layout.count())): 
            self.answers_layout.itemAt(i).widget().setParent(None)
        
        # Generate new question
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.correct_answer = self.num1 * self.num2
        
        # Update question label with default style
        self.question_label.setText(f"{self.num1} × {self.num2} = ?")
        self.question_label.setStyleSheet(styles.QUESTION_LABEL_STYLE)
        
        # Generate answer options
        options = [self.correct_answer]
        while len(options) < 4:
            wrong_answer = self.correct_answer + random.randint(-5, 5)
            if wrong_answer != self.correct_answer and wrong_answer not in options:
                options.append(wrong_answer)
        
        random.shuffle(options)
        
        # Create new answer buttons
        for option in options:
            button = QPushButton(str(option))
            button.setMinimumSize(*styles.ANSWER_BUTTON_SIZE)
            button.setStyleSheet(styles.ANSWER_BUTTON_STYLE)
            button.clicked.connect(lambda checked, ans=option: self.check_answer(ans))
            self.answers_layout.addWidget(button, alignment=Qt.AlignCenter)
        
        # Hide feedback and next button
        self.feedback_label.setText("")
        self.next_button.hide()
    
    def check_answer(self, selected_answer):
        """Check the answer and provide feedback."""
        # Disable all answer buttons
        for i in range(self.answers_layout.count()):
            button = self.answers_layout.itemAt(i).widget()
            button.setEnabled(False)
        
        if selected_answer == self.correct_answer:
            self.feedback_label.setText(styles.CORRECT_FEEDBACK)
            self.feedback_label.setStyleSheet(styles.FEEDBACK_CORRECT_STYLE)
            self.question_label.setText(f"{self.num1} × {self.num2} = {self.correct_answer}")
            self.question_label.setStyleSheet(styles.QUESTION_LABEL_STYLE + "color: green;")
        else:
            self.feedback_label.setText(styles.INCORRECT_FEEDBACK.format(self.correct_answer))
            self.feedback_label.setStyleSheet(styles.FEEDBACK_INCORRECT_STYLE)
            self.question_label.setText(f"{self.num1} × {self.num2} = {self.correct_answer}")
            self.question_label.setStyleSheet(styles.QUESTION_LABEL_STYLE + "color: red;")
        
        self.next_button.show() 