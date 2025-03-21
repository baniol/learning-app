from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
import sys
import quizzes.styles as styles
from quizzes.menu import MainMenu
from quizzes.quiz_container import QuizContainer
# Import all quiz classes that might be created through QUIZ_TYPE_MAP
from quizzes.types.multiplication_quiz import MultiplicationQuiz
from quizzes.types.addition_quiz import AdditionQuiz
from quizzes.types.custom_quizzes import SmallMultiplicationQuiz, SubtractionQuiz

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(styles.WINDOW_TITLE)
        self.setGeometry(styles.WINDOW_INITIAL_POSITION[0], styles.WINDOW_INITIAL_POSITION[1], 
                         styles.WINDOW_INITIAL_SIZE[0], styles.WINDOW_INITIAL_SIZE[1])
        self.setMinimumSize(styles.WINDOW_MINIMUM_SIZE[0], styles.WINDOW_MINIMUM_SIZE[1])

        # Central widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(styles.MAIN_BORDER_STYLE)
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(styles.MAIN_LAYOUT_MARGINS[0], 0, 
                                           styles.MAIN_LAYOUT_MARGINS[2], styles.MAIN_LAYOUT_MARGINS[3])
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        self.menu = MainMenu()
        self.quiz_container = QuizContainer()
        
        self.menu.quiz_selected.connect(self.on_quiz_selected)
        self.quiz_container.return_to_menu.connect(self.show_menu)
        
        self.main_layout.addWidget(self.menu, 1)
        self.main_layout.addWidget(self.quiz_container, 1)
        self.quiz_container.hide()

    def on_quiz_selected(self, name):
        """Handle quiz selection from the menu."""
        quiz_class_name = styles.QUIZ_TYPE_MAP.get(name)
        if quiz_class_name:
            quiz_class = globals()[quiz_class_name]
            quiz = quiz_class(
                total_questions=styles.DEFAULT_QUIZ_QUESTIONS,
                show_questions_control=False
            )
            self.show_quiz(quiz)

    def show_quiz(self, quiz):
        """Show the selected quiz."""
        self.quiz_container.set_quiz(quiz)
        self.menu.hide()
        self.quiz_container.show()

    def show_menu(self):
        """Return to the main menu."""
        self.quiz_container.hide()
        self.menu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

