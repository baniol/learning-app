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
# Import user management
from quizzes.database.users import get_all_users, get_user
from quizzes.components.user_dialog import UserDialog
from quizzes.components.navigation_bar import NavigationBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        
        # Add top navigation bar with user selection
        self.setup_top_bar()

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
        
        # Set current user - default to Anonymous (ID 1)
        self.current_user_id = 1
        self.current_user = get_user(self.current_user_id) or {"id": 1, "username": "anonymous", "display_name": "Anonymous"}

    def setup_top_bar(self):
        """Set up the top navigation bar with user selection."""
        # Top bar container
        top_container = QWidget()
        top_container.setFixedHeight(50)
        top_container.setStyleSheet(styles.NAV_BAR_BORDER_STYLE)
        
        # Top bar layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 5, 10, 5)
        top_container.setLayout(top_layout)
        
        # App title
        title_label = QWidget()
        title_label.setFixedWidth(200)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label.setLayout(title_layout)
        
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt
        app_title = QLabel("Quiz App")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(app_title)
        
        top_layout.addWidget(title_label)
        
        # Add spacer
        top_layout.addStretch(1)
        
        # Navigation bar for user dropdown
        self.nav_bar = NavigationBar(lambda: None)  # No return callback needed
        self.nav_bar.setFixedHeight(40)
        
        # Get users from database
        try:
            users = get_all_users()
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Failed to load users: {str(e)}")
            users = [{"id": 1, "display_name": "Anonymous"}]
        
        # Add user dropdown
        self.user_dropdown = self.nav_bar.add_user_dropdown(users)
        self.nav_bar.user_changed.connect(self.on_user_changed)
        
        top_layout.addWidget(self.nav_bar)
        
        # Add to main layout
        self.main_layout.addWidget(top_container)
    
    def on_user_changed(self, user_id):
        """Handle user selection changes."""
        print(f"User changed to ID: {user_id}")
        
        # If it's the special "Add New User" option
        if user_id == -1:
            # Add new user was selected
            print("Add new user selected, opening dialog...")
            result = UserDialog.create_user(self)
            print(f"Dialog result: {result}")
            
            if result:
                # Dialog was accepted and user was created
                new_user_id, username, display_name = result
                print(f"New user created: {new_user_id}, {username}, {display_name}")
                
                # Update the dropdown with the new user selected
                self.refresh_user_dropdown(new_user_id)
                
                # Set as current user
                self.current_user_id = new_user_id
                self.current_user = {
                    "id": new_user_id,
                    "username": username,
                    "display_name": display_name
                }
            else:
                # Dialog was canceled or failed
                print("User creation canceled or failed")
                # Reset to the previously selected user
                try:
                    # Find the index for the current user ID
                    for i in range(self.user_dropdown.count()):
                        if self.user_dropdown.itemData(i) == self.current_user_id:
                            self.user_dropdown.setCurrentIndex(i)
                            break
                except Exception as e:
                    print(f"Error resetting user dropdown: {str(e)}")
                    # If all else fails, set to the first item
                    if self.user_dropdown.count() > 0:
                        self.user_dropdown.setCurrentIndex(0)
        else:
            # Regular user selection
            self.current_user_id = user_id
            self.current_user = get_user(user_id) or {"id": user_id}
    
    def refresh_user_dropdown(self, select_user_id=None):
        """Refresh the user dropdown with current users."""
        try:
            users = get_all_users()
            
            # Clear and repopulate dropdown
            current_index = 0
            self.user_dropdown.clear()
            
            for i, user in enumerate(users):
                self.user_dropdown.addItem(user['display_name'], user['id'])
                if select_user_id and user['id'] == select_user_id:
                    current_index = i
            
            # Add the "Add New User" option
            self.user_dropdown.addItem("+ Add New User", -1)
            
            # Set the selected index
            if select_user_id:
                self.user_dropdown.setCurrentIndex(current_index)
                
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Failed to refresh users: {str(e)}")
    
    def on_quiz_selected(self, name):
        """Handle quiz selection from the menu."""
        # Special case for Scores
        if name == "Scores":
            self.show_scores()
            return

        quiz_class_name = QUIZ_TYPE_MAP.get(name)
        if quiz_class_name:
            # Use the quiz manager to create the quiz
            quiz = quiz_manager.create_quiz(
                quiz_class_name,
                total_questions=DEFAULT_QUIZ_QUESTIONS,
                show_questions_control=False
            )
            if quiz:
                # Set current user for the quiz
                if hasattr(quiz, 'set_player_name'):
                    quiz.set_player_name(self.current_user.get('display_name', 'Anonymous'))
                self.show_quiz(quiz)

    def show_quiz(self, quiz):
        """Show the selected quiz."""
        self.quiz_container.set_quiz(quiz)
        self.menu.hide()
        self.scores_page.hide()
        self.quiz_container.show()

    def show_scores(self):
        """Show the scores page."""
        self.scores_page.refresh()
        self.menu.hide()
        self.quiz_container.hide()
        self.scores_page.show()

    def show_menu(self):
        """Return to the main menu."""
        self.quiz_container.hide()
        self.scores_page.hide()
        self.menu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

