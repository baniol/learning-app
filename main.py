from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
import sys
import random
from quizzes.multiplication_quiz import MultiplicationQuiz
from quizzes.addition_quiz import AdditionQuiz
from quizzes.custom_quizzes import SmallMultiplicationQuiz, SubtractionQuiz
from PySide6.QtCore import Qt
from quizzes.styles import (
    WINDOW_TITLE, WINDOW_INITIAL_POSITION, WINDOW_INITIAL_SIZE, WINDOW_MINIMUM_SIZE,
    MAIN_LAYOUT_MARGINS, MAIN_LAYOUT_SPACING, MENU_LAYOUT_SPACING,
    MENU_BUTTON_SIZE, MENU_BUTTON_STYLE, QUIZ_LAYOUT_SPACING, QUIZ_LAYOUT_MARGINS,
    ANSWERS_LAYOUT_SPACING, ANSWER_BUTTON_SIZE, ANSWER_BUTTON_STYLE,
    QUESTION_LABEL_STYLE, FEEDBACK_LABEL_STYLE, FEEDBACK_CORRECT_STYLE, FEEDBACK_INCORRECT_STYLE,
    MENU_ITEMS, QUIZ_TYPE_MAP, DEFAULT_QUIZ_QUESTIONS, CORRECT_FEEDBACK, INCORRECT_FEEDBACK,
    MAIN_BORDER_STYLE, MENU_CONTAINER_BORDER_STYLE, QUIZ_CONTAINER_BORDER_STYLE, ANSWERS_CONTAINER_BORDER_STYLE
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(WINDOW_INITIAL_POSITION[0], WINDOW_INITIAL_POSITION[1], 
                         WINDOW_INITIAL_SIZE[0], WINDOW_INITIAL_SIZE[1])
        self.setMinimumSize(WINDOW_MINIMUM_SIZE[0], WINDOW_MINIMUM_SIZE[1])

        # Central widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(MAIN_BORDER_STYLE)
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(*MAIN_LAYOUT_MARGINS)
        self.main_layout.setSpacing(MAIN_LAYOUT_SPACING)
        self.central_widget.setLayout(self.main_layout)

        # Menu container widget
        self.menu_widget = QWidget()
        self.menu_widget.setStyleSheet(MENU_CONTAINER_BORDER_STYLE)
        self.menu_layout = QGridLayout()
        self.menu_layout.setSpacing(MENU_LAYOUT_SPACING)
        self.menu_widget.setLayout(self.menu_layout)
        self.main_layout.addWidget(self.menu_widget)

        # Add buttons to grid (2 rows, 3 columns)
        for i, item in enumerate(MENU_ITEMS):
            button = QPushButton(item)
            button.setMinimumSize(*MENU_BUTTON_SIZE)
            button.setStyleSheet(MENU_BUTTON_STYLE)
            button.clicked.connect(lambda checked, name=item: self.on_button_click(name))
            self.menu_layout.addWidget(button, i // 3, i % 3)

        # Quiz widgets (initially hidden)
        self.quiz_widget = QWidget()
        self.quiz_widget.setStyleSheet(QUIZ_CONTAINER_BORDER_STYLE)
        self.quiz_layout = QVBoxLayout()
        self.quiz_layout.setSpacing(QUIZ_LAYOUT_SPACING)
        self.quiz_widget.setLayout(self.quiz_layout)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet(QUESTION_LABEL_STYLE)
        self.question_label.setAlignment(Qt.AlignCenter)  # Center the question
        self.quiz_layout.addWidget(self.question_label)
        
        # Answer buttons container
        self.answers_widget = QWidget()
        self.answers_widget.setStyleSheet(ANSWERS_CONTAINER_BORDER_STYLE)
        self.answers_layout = QVBoxLayout()
        self.answers_layout.setSpacing(ANSWERS_LAYOUT_SPACING)
        self.answers_widget.setLayout(self.answers_layout)
        self.quiz_layout.addWidget(self.answers_widget)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet(FEEDBACK_LABEL_STYLE)
        self.feedback_label.setAlignment(Qt.AlignCenter)  # Center the feedback
        self.quiz_layout.addWidget(self.feedback_label)
        
        # Next question button
        self.next_button = QPushButton("Next Question")
        self.next_button.setMinimumSize(*ANSWER_BUTTON_SIZE)
        self.next_button.clicked.connect(self.generate_new_question)
        self.next_button.hide()
        self.quiz_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)  # Center the button
        
        # Add quiz widget to main layout
        self.main_layout.addWidget(self.quiz_widget)
        self.quiz_widget.hide()

    def on_button_click(self, name):
        if name in QUIZ_TYPE_MAP:
            quiz_class = globals()[QUIZ_TYPE_MAP[name]]
            self.show_quiz(quiz_class(
                total_questions=DEFAULT_QUIZ_QUESTIONS,
                show_questions_control=False
            ))
        else:
            print(f"{name} clicked")

    def show_quiz(self, quiz):
        # Clear previous quiz if any
        for i in reversed(range(self.quiz_layout.count())): 
            self.quiz_layout.itemAt(i).widget().setParent(None)
        
        # Add new quiz with minimal margins
        self.quiz_layout.setContentsMargins(*QUIZ_LAYOUT_MARGINS)
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
        self.question_label.setStyleSheet(QUESTION_LABEL_STYLE)
        
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
            button.setMinimumSize(*ANSWER_BUTTON_SIZE)
            button.setStyleSheet(ANSWER_BUTTON_STYLE)
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
            self.feedback_label.setText(CORRECT_FEEDBACK)
            self.feedback_label.setStyleSheet(FEEDBACK_CORRECT_STYLE)
            self.question_label.setText(f"{self.num1} × {self.num2} = {self.correct_answer}")
            self.question_label.setStyleSheet(QUESTION_LABEL_STYLE + "color: green;")
        else:
            self.feedback_label.setText(INCORRECT_FEEDBACK.format(self.correct_answer))
            self.feedback_label.setStyleSheet(FEEDBACK_INCORRECT_STYLE)
            self.question_label.setText(f"{self.num1} × {self.num2} = {self.correct_answer}")
            self.question_label.setStyleSheet(QUESTION_LABEL_STYLE + "color: red;")
        
        self.next_button.show()

    def show_menu(self):
        self.quiz_widget.hide()
        self.menu_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

