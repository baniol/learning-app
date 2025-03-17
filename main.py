from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
import sys
import random
from quizzes.multiplication_quiz import MultiplicationQuiz
from quizzes.addition_quiz import AdditionQuiz
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Math Quiz")
        self.setGeometry(100, 100, 800, 600)  # Larger initial size
        self.setMinimumSize(600, 400)  # Set minimum window size

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Add some padding
        self.main_layout.setSpacing(20)  # Add spacing between widgets
        self.central_widget.setLayout(self.main_layout)

        # Menu container widget
        self.menu_widget = QWidget()
        self.menu_layout = QGridLayout()
        self.menu_layout.setSpacing(20)  # Add spacing between buttons
        self.menu_widget.setLayout(self.menu_layout)
        self.main_layout.addWidget(self.menu_widget)

        # Menu Items
        menu_items = [
            "Multiplication Quiz", "Addition Quiz", "Item 3",
            "Item 4", "Item 5", "Item 6"
        ]

        # Add buttons to grid (2 rows, 3 columns)
        for i, item in enumerate(menu_items):
            button = QPushButton(item)
            button.setMinimumSize(200, 120)  # Set minimum size instead of fixed
            button.clicked.connect(lambda checked, name=item: self.on_button_click(name))
            self.menu_layout.addWidget(button, i // 3, i % 3)

        # Quiz widgets (initially hidden)
        self.quiz_widget = QWidget()
        self.quiz_layout = QVBoxLayout()
        self.quiz_layout.setSpacing(20)  # Add spacing between widgets
        self.quiz_widget.setLayout(self.quiz_layout)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.question_label.setAlignment(Qt.AlignCenter)  # Center the question
        self.quiz_layout.addWidget(self.question_label)
        
        # Answer buttons container
        self.answers_widget = QWidget()
        self.answers_layout = QVBoxLayout()
        self.answers_layout.setSpacing(10)  # Add spacing between buttons
        self.answers_widget.setLayout(self.answers_layout)
        self.quiz_layout.addWidget(self.answers_widget)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet("font-size: 18px;")
        self.feedback_label.setAlignment(Qt.AlignCenter)  # Center the feedback
        self.quiz_layout.addWidget(self.feedback_label)
        
        # Next question button
        self.next_button = QPushButton("Next Question")
        self.next_button.setMinimumSize(200, 50)  # Set minimum size instead of fixed
        self.next_button.clicked.connect(self.generate_new_question)
        self.next_button.hide()
        self.quiz_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)  # Center the button
        
        # Add quiz widget to main layout
        self.main_layout.addWidget(self.quiz_widget)
        self.quiz_widget.hide()

    def on_button_click(self, name):
        if name == "Multiplication Quiz":
            self.show_quiz(MultiplicationQuiz(total_questions=20))
        elif name == "Addition Quiz":
            self.show_quiz(AdditionQuiz(total_questions=20))
        else:
            print(f"{name} clicked")

    def show_quiz(self, quiz):
        # Clear previous quiz if any
        for i in reversed(range(self.quiz_layout.count())): 
            self.quiz_layout.itemAt(i).widget().setParent(None)
        
        # Add new quiz with minimal margins
        self.quiz_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.quiz_layout.addWidget(quiz)
        self.menu_widget.hide()
        self.quiz_widget.show()
        quiz.generate_new_question()

    def generate_new_question(self):
        # Clear previous answer buttons
        for i in reversed(range(self.answers_layout.count())): 
            self.answers_layout.itemAt(i).widget().setParent(None)
        
        # Generate new question
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.correct_answer = self.num1 * self.num2
        
        # Update question label with default style
        self.question_label.setText(f"{self.num1} × {self.num2} = ?")
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
            button.setMinimumSize(200, 50)  # Set minimum size instead of fixed
            button.clicked.connect(lambda checked, ans=option: self.check_answer(ans))
            self.answers_layout.addWidget(button, alignment=Qt.AlignCenter)  # Center the buttons
        
        # Hide feedback and next button
        self.feedback_label.setText("")
        self.next_button.hide()

    def check_answer(self, selected_answer):
        # Disable all answer buttons
        for i in range(self.answers_layout.count()):
            button = self.answers_layout.itemAt(i).widget()
            button.setEnabled(False)
        
        if selected_answer == self.correct_answer:
            self.feedback_label.setText("Super! Dobra robota!")
            self.feedback_label.setStyleSheet("font-size: 18px; color: green;")
            self.question_label.setText(f"{self.num1} × {self.num2} = {self.correct_answer}")
            self.question_label.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")
        else:
            self.feedback_label.setText(f"Nie! Poprawna odpowiedź to {self.correct_answer}")
            self.feedback_label.setStyleSheet("font-size: 18px; color: red;")
            self.question_label.setText(f"{self.num1} × {self.num2} = {self.correct_answer}")
            self.question_label.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
        
        self.next_button.show()

    def show_menu(self):
        self.quiz_widget.hide()
        self.menu_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

