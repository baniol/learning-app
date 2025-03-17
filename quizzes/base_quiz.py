from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import random

class BaseQuiz(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.question_label)
        
        # Answer buttons container
        self.answers_widget = QWidget()
        self.answers_layout = QVBoxLayout()
        self.answers_widget.setLayout(self.answers_layout)
        self.layout.addWidget(self.answers_widget)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.feedback_label)
        
        # Next question button
        self.next_button = QPushButton("Next Question")
        self.next_button.setFixedSize(200, 50)
        self.next_button.clicked.connect(self.generate_new_question)
        self.next_button.hide()
        self.layout.addWidget(self.next_button)

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
        
        # Create new answer buttons
        for option in options:
            button = QPushButton(str(option))
            button.setFixedSize(200, 50)
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