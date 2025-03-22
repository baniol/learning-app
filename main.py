from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
import sys
import quizzes.styles as styles
from quizzes.constants import WINDOW_TITLE
from quizzes.mappings import QUIZ_TYPE_MAP, DEFAULT_QUIZ_QUESTIONS
from quizzes.menu import MainMenu
from quizzes.quiz_container import QuizContainer
from quizzes.quiz_manager import quiz_manager
# Import all quiz classes that might be created through QUIZ_TYPE_MAP
from quizzes.types.multiplication_quiz import MultiplicationQuiz
from quizzes.types.addition_quiz import AdditionQuiz
from quizzes.types.custom_quizzes import SmallMultiplicationQuiz, SubtractionQuiz
# Import scores page
from quizzes.scores_page import ScoresPage
# Import user manager and components
from quizzes.user_manager import UserManager
from quizzes.components import TopBar
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
# Import debug module
from quizzes.debug import set_debug_mode, log

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        log("Main", "Initializing MainWindow")
        self.setWindowTitle(WINDOW_TITLE)
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
        
        # Initialize user manager - debug mode is handled by the debug module
        self.user_manager = UserManager(self)
        self.user_manager.user_changed.connect(self.on_user_data_changed)
        
        # Add top navigation bar with user selection
        self.top_bar = TopBar(self.user_manager, self)
        self.main_layout.addWidget(self.top_bar)

        # Content
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.main_layout.addLayout(self.content_layout)
        
        self.menu = MainMenu()
        self.quiz_container = QuizContainer()
        self.scores_page = ScoresPage()
        
        self.menu.quiz_selected.connect(self.on_quiz_selected)
        self.quiz_container.return_to_menu.connect(self.show_menu)
        self.scores_page.return_to_menu.connect(self.show_menu)
        
        self.content_layout.addWidget(self.menu, 1)
        self.content_layout.addWidget(self.quiz_container, 1)
        self.content_layout.addWidget(self.scores_page, 1)
        
        self.quiz_container.hide()
        self.scores_page.hide()
        
        log("Main", "MainWindow initialization complete")

    def on_user_data_changed(self, user_data):
        """Handle user data changes from UserManager."""
        log("Main", f"User data changed: {user_data}")
        # Update any UI elements that depend on the current user
        # This is called when the user selection changes
    
    def on_quiz_selected(self, name):
        """Handle quiz selection from the menu."""
        log("Main", f"Quiz selected: {name}")
        # Special case for Scores
        if name == "Scores":
            self.show_scores()
            return

        quiz_class_name = QUIZ_TYPE_MAP.get(name)
        if quiz_class_name:
            log("Main", f"Creating quiz of type: {quiz_class_name}")
            # Use the quiz manager to create the quiz
            quiz = quiz_manager.create_quiz(
                quiz_class_name,
                total_questions=DEFAULT_QUIZ_QUESTIONS,
                show_questions_control=False
            )
            if quiz:
                # Set current user for the quiz
                current_user = self.user_manager.get_current_user()
                if hasattr(quiz, 'set_player_name'):
                    quiz.set_player_name(current_user.get('display_name', 'Anonymous'))
                self.show_quiz(quiz)

    def show_quiz(self, quiz):
        """Show the selected quiz."""
        log("Main", "Showing quiz")
        self.quiz_container.set_quiz(quiz)
        self.menu.hide()
        self.scores_page.hide()
        self.quiz_container.show()

    def show_scores(self):
        """Show the scores page."""
        log("Main", "Showing scores page")
        self.scores_page.refresh()
        self.menu.hide()
        self.quiz_container.hide()
        self.scores_page.show()

    def show_menu(self):
        """Return to the main menu."""
        log("Main", "Showing main menu")
        self.quiz_container.hide()
        self.scores_page.hide()
        self.menu.show()

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        set_debug_mode(True)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

