"""
Base quiz class that provides common functionality for all quizzes.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QProgressBar, QGridLayout, QSizePolicy, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIntValidator
import random
from typing import List, Optional, Callable, Union, Dict, Any
from .styles import (
    QUESTION_LABEL_STYLE, QUESTION_CORRECT_STYLE, QUESTION_INCORRECT_STYLE,
    FEEDBACK_LABEL_STYLE, FEEDBACK_CORRECT_STYLE, FEEDBACK_INCORRECT_STYLE,
    ANSWER_BUTTON_STYLE, NEXT_BUTTON_STYLE, MAIN_BORDER_STYLE,
    DEFAULT_SPACING, BUTTON_SPACING, RETURN_BUTTON_STYLE,
    ANSWER_INPUT_STYLE, SUBMIT_BUTTON_STYLE
)
from .constants import (
    PROGRESS_LABEL_TEXT, SCORE_LABEL_TEXT, RESULTS_TITLE_TEXT, RESULTS_SCORE_TEXT,
    NEW_QUIZ_TOOLTIP, MENU_RETURN_TOOLTIP, NEXT_BUTTON_ICON, RESTART_BUTTON_ICON,
    HOME_BUTTON_ICON, CORRECT_BUTTON_ICON, MAIN_WINDOW_ERROR,
    CORRECT_FEEDBACK, INCORRECT_FEEDBACK
)
from .mappings import DEFAULT_QUIZ_QUESTIONS
from .components import ScoreIndicator
# Import database module for score saving
from .database.scores import save_score

class BaseQuiz(QWidget):
    """Base class for all quizzes with common UI and functionality.
    
    This class provides the foundation for all quiz types, with shared UI components
    and logic for handling questions, answers, scoring, and navigation. Specific quiz
    types should inherit from this class and override the necessary methods.
    """
    
    def __init__(self, parent=None, total_questions=DEFAULT_QUIZ_QUESTIONS, show_visual_aid=True, show_questions_control=True):
        """Initialize the quiz with basic UI components.
        
        Args:
            parent: Parent widget
            total_questions: The total number of questions to include in the quiz
            show_visual_aid: Whether to show visual aids
            show_questions_control: Whether to show question control options
        """
        super().__init__(parent)
        self.setStyleSheet(MAIN_BORDER_STYLE)
        
        print(f"DEBUG: Initializing BaseQuiz with {total_questions} questions")
        
        # Quiz session state
        self.total_questions: int = total_questions
        self.current_question: int = 0  # Will be set to 1 by next_question
        self.correct_answers: int = 0
        self.quiz_completed: bool = False
        self.input_mode: bool = False  # Default to button mode
        self.show_visual_aid: bool = show_visual_aid
        self.show_questions_control: bool = show_questions_control
        self.player_name: str = "Anonymous"  # Default player name
        
        # Quiz problem state
        self.num1: int = 0
        self.num2: int = 0
        self.expected_answer: Optional[int] = None
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)
        
        self._create_progress_container()
        self._create_question_container()
        self._create_interaction_area()
        self._create_results_screen()
        
        # Initialize UI components
        self.init_ui()
        
        # Setup initial UI state before generating first question
        self.progress_bar.setValue(0)
        self.progress_label.setText(PROGRESS_LABEL_TEXT.format(0, self.total_questions))
        
        print(f"DEBUG: BaseQuiz initialization completed, calling next_question()")
        
        # Generate first question using next_question to ensure counter starts at 1
        self.next_question()
        
        print(f"DEBUG: BaseQuiz after next_question call, current_question: {self.current_question}")
    
    def _create_progress_container(self) -> None:
        """Create the progress bar and score indicator container."""
        # Progress bar
        self.progress_container = QWidget()
        self.progress_container.setFixedHeight(50)
        self.progress_layout = QHBoxLayout()
        self.progress_layout.setContentsMargins(5, 5, 5, 5)  # Reduce internal margins
        self.progress_container.setLayout(self.progress_layout)
        
        # Progress bar with label
        self.progress_label = QLabel(PROGRESS_LABEL_TEXT.format(0, self.total_questions))
        self.progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.total_questions)
        self.progress_bar.setValue(0)
        self.progress_layout.addWidget(self.progress_bar)
        
        # Score indicator with label
        score_container = QWidget()
        score_layout = QHBoxLayout()
        score_layout.setContentsMargins(0, 0, 0, 0)
        score_layout.setSpacing(5)
        score_container.setLayout(score_layout)
        
        score_label = QLabel(SCORE_LABEL_TEXT)
        score_layout.addWidget(score_label)
        
        self.score_indicator = ScoreIndicator()
        score_layout.addWidget(self.score_indicator)
        
        self.progress_layout.addWidget(score_container)
        
        self.main_layout.addWidget(self.progress_container)
    
    def _create_question_container(self) -> None:
        """Create the question display area."""
        # Question label (with stretch to adapt to window height)
        self.question_label = QLabel()
        self.question_label.setStyleSheet(QUESTION_LABEL_STYLE)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setMinimumHeight(60)  # Minimum height instead of fixed
        # Allow question label to expand vertically when window is resized
        self.question_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.question_label)
    
    def _create_interaction_area(self) -> None:
        """Create the interaction area with answer buttons, feedback, and next button."""
        # Create a single row widget with 3 columns for answers, feedback, and next button
        self.interaction_widget = QWidget()
        # Fix the height of the interaction widget
        self.interaction_widget.setFixedHeight(140)  # Fixed height for the entire row
        self.interaction_layout = QHBoxLayout()
        self.interaction_layout.setSpacing(DEFAULT_SPACING)
        self.interaction_widget.setLayout(self.interaction_layout)
        
        # Answer buttons container - grid layout
        self.answers_widget = QWidget()
        self.answers_layout = QGridLayout()
        self.answers_layout.setSpacing(BUTTON_SPACING)
        self.answers_widget.setLayout(self.answers_layout)
        self.interaction_layout.addWidget(self.answers_widget, 2)  # 2 parts for answers
        
        # Feedback label container
        self.feedback_container = QWidget()
        self.feedback_layout = QVBoxLayout()
        self.feedback_layout.setContentsMargins(10, 0, 10, 0)  # Add some horizontal padding
        self.feedback_container.setLayout(self.feedback_layout)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setStyleSheet(FEEDBACK_LABEL_STYLE)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setWordWrap(True)  # Allow text wrapping
        self.feedback_label.setMaximumHeight(100)  # Limit the maximum height
        self.feedback_layout.addWidget(self.feedback_label)
        self.interaction_layout.addWidget(self.feedback_container, 2)  # 2 parts for feedback
        
        # Next button container
        self.next_button_container = QWidget()
        self.next_button_layout = QVBoxLayout()
        self.next_button_layout.setContentsMargins(0, 0, 0, 0)
        self.next_button_container.setLayout(self.next_button_layout)
        
        # Next question button
        self.next_button = QPushButton(NEXT_BUTTON_ICON)  # Right arrow emoji
        self.next_button.setFixedSize(60, 60)  # Fixed size
        self.next_button.setStyleSheet(NEXT_BUTTON_STYLE)
        self.next_button.setFont(QFont("Arial", 20))  # Adjust font size for the emoji
        self.next_button.clicked.connect(self.on_next_button_click)
        self.next_button.setEnabled(False)
        self.next_button_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
        self.interaction_layout.addWidget(self.next_button_container, 1)  # 1 part for button
        
        # Add the interaction widget to the main layout
        self.main_layout.addWidget(self.interaction_widget)
    
    def _create_results_screen(self) -> None:
        """Create the results screen shown at the end of the quiz."""
        # Results widget (initially hidden)
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_layout.setSpacing(DEFAULT_SPACING * 2)  # Increase spacing for better appearance
        self.results_widget.setLayout(self.results_layout)
        
        # Add some space at the top to center content vertically
        self.results_layout.addStretch(1)
        
        self.results_title = QLabel(RESULTS_TITLE_TEXT)
        self.results_title.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.results_title.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(self.results_title)
        
        self.results_score = QLabel()
        self.results_score.setStyleSheet("font-size: 20px;")
        self.results_score.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(self.results_score)
        
        # Button container for results screen
        self.results_buttons = QWidget()
        self.results_buttons_layout = QHBoxLayout()
        self.results_buttons_layout.setSpacing(DEFAULT_SPACING * 2)  # More space between buttons
        self.results_buttons.setLayout(self.results_buttons_layout)
        
        # Restart button with icon
        self.restart_button = QPushButton(RESTART_BUTTON_ICON)  # Restart emoji
        self.restart_button.setMinimumSize(80, 80)
        self.restart_button.setStyleSheet(NEXT_BUTTON_STYLE)
        self.restart_button.setFont(QFont("Arial", 20))
        self.restart_button.setToolTip(NEW_QUIZ_TOOLTIP)
        self.restart_button.clicked.connect(self.restart_quiz)
        self.results_buttons_layout.addWidget(self.restart_button)
        
        # Home button for returning to menu
        self.menu_button = QPushButton(HOME_BUTTON_ICON)  # Home emoji
        self.menu_button.setMinimumSize(80, 80)
        self.menu_button.setStyleSheet(RETURN_BUTTON_STYLE)
        self.menu_button.setFont(QFont("Arial", 20))
        self.menu_button.setToolTip(MENU_RETURN_TOOLTIP)
        self.menu_button.clicked.connect(self.return_to_menu)
        self.results_buttons_layout.addWidget(self.menu_button)
        
        self.results_layout.addWidget(self.results_buttons, alignment=Qt.AlignCenter)
        
        # Add some space at the bottom to center content vertically
        self.results_layout.addStretch(1)
        
        # Add the results widget to the main layout (initially hidden)
        self.main_layout.addWidget(self.results_widget)
        self.results_widget.hide()

    def on_next_button_click(self) -> None:
        """Handle next button click based on quiz state."""
        print(f"DEBUG: on_next_button_click called, current_question: {self.current_question}")
        
        if self.quiz_completed:
            self.restart_quiz()
        else:
            # Only increment if not the first question (which is handled by next_question)
            if self.current_question > 0:
                self.current_question += 1
                print(f"DEBUG: Incremented current_question to: {self.current_question}")
            
            # Check if we've exceeded total_questions
            if self.current_question > self.total_questions:
                self.show_results()
            else:
                self.next_question()

    def restart_quiz(self) -> None:
        """Restart the quiz with a new set of questions."""
        # Reset quiz state
        self.current_question = 0  # Will be set to 1 by next_question
        self.correct_answers = 0
        self.quiz_completed = False
        
        # Reset UI
        self.progress_bar.setValue(0)
        self.progress_label.setText(PROGRESS_LABEL_TEXT.format(0, self.total_questions))
        self.score_indicator.set_score(0, self.total_questions, 0)
        
        # Hide results, show quiz UI
        self.results_widget.hide()
        self.question_label.show()
        self.interaction_widget.show()
        
        # Generate first question with correct counting
        self.next_question()

    def return_to_menu(self) -> None:
        """Return to the main menu."""
        # Find the main window (which should be the top-level parent)
        main_window = self.window()
        if main_window and hasattr(main_window, 'show_menu'):
            main_window.show_menu()
        else:
            print(MAIN_WINDOW_ERROR)

    def generate_new_question(self) -> None:
        """Generate a new question and update the UI."""
        print(f"DEBUG: generate_new_question called, current_question before: {self.current_question}")
        
        # Note: We don't increment current_question here anymore
        # The next_question method handles incrementing the counter
        
        # Update UI
        self.progress_bar.setValue(self.current_question)
        print(f"DEBUG: Set progress bar to: {self.current_question}")
        self.progress_label.setText(PROGRESS_LABEL_TEXT.format(self.current_question, self.total_questions))
        
        # Check if quiz is complete
        if self.current_question > self.total_questions:
            self.show_results()
            return
        
        # Clear previous answer buttons
        self.clear_answer_buttons()
        
        # Generate new question
        self.generate_numbers()
        self.expected_answer = self.calculate_answer()
        
        # Update question label with default style
        self.question_label.setText(self.format_question())
        self.question_label.setStyleSheet(QUESTION_LABEL_STYLE)
        
        # Generate answer options
        options = self.generate_answer_options()
        
        # Create answer buttons/inputs
        self.create_answer_buttons(options)
        
        # Additional setup for specific quiz types
        self.on_new_question()
    
    def show_results(self) -> None:
        """Display the results screen at the end of the quiz."""
        self.quiz_completed = True
        
        # Calculate score percentage
        score_percent = (self.correct_answers / self.total_questions) * 100
        
        # Update results widgets
        self.results_title.setText("Quiz Complete!")
        self.results_score.setText("{}/{} ({:.1f}%)".format(
            self.correct_answers,
            self.total_questions,
            score_percent
        ))
        
        # Set color based on score
        if score_percent >= 80:
            self.results_score.setStyleSheet("font-size: 20px; color: green;")
        elif score_percent >= 60:
            self.results_score.setStyleSheet("font-size: 20px; color: orange;")
        else:
            self.results_score.setStyleSheet("font-size: 20px; color: red;")
        
        # Save score to database
        quiz_type = self.__class__.__name__
        save_score(quiz_type, self.correct_answers, self.total_questions, self.player_name)
        
        # Hide quiz UI elements
        self.question_label.hide()
        self.interaction_widget.hide()
        
        # Show results
        self.results_widget.show()
    
    def generate_numbers(self) -> None:
        """Generate random numbers for the question. Override in subclasses if needed."""
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
    
    def on_new_question(self) -> None:
        """Hook for subclasses to perform additional setup after generating a new question."""
        pass
    
    def clear_answer_buttons(self) -> None:
        """Clear all answer buttons or input fields from the layout."""
        for i in reversed(range(self.answers_layout.count())): 
            widget = self.answers_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
    
    def generate_answer_options(self) -> List[int]:
        """Generate answer options including the correct answer and distractors.
        
        Returns:
            List of answer options (integers)
        """
        options = [self.expected_answer]
        
        # Generate 3 additional options (distractors)
        while len(options) < 4:
            # Generate a distractor within a reasonable range around the correct answer
            option = random.randint(max(1, self.expected_answer - 5), self.expected_answer + 5)
            if option != self.expected_answer and option not in options:
                options.append(option)
        
        # Shuffle options
        random.shuffle(options)
        return options
    
    def create_answer_buttons(self, options: List[int]) -> None:
        """Create buttons for each answer option in a 2x2 grid or input field based on mode.
        
        Args:
            options: List of answer options (integers)
        """
        if self.input_mode:
            self._create_input_field()
        else:
            self._create_option_buttons(options)

    def _create_option_buttons(self, options: List[int]) -> None:
        """Create buttons for each answer option in a 2x2 grid.
        
        Args:
            options: List of answer options (integers)
        """
        for i, option in enumerate(options):
            row, col = divmod(i, 2)
            button = QPushButton(str(option))
            button.setStyleSheet(ANSWER_BUTTON_STYLE)
            button.setMinimumHeight(50)
            button.clicked.connect(lambda checked, ans=option: self.check_answer(ans))
            self.answers_layout.addWidget(button, row, col)

    def _create_input_field(self) -> None:
        """Create an input field and submit button for manual answer entry."""
        # Create input field
        self.answer_input = QLineEdit()
        self.answer_input.setStyleSheet(ANSWER_INPUT_STYLE)
        self.answer_input.setPlaceholderText("Type your answer...")
        self.answer_input.setMinimumHeight(50)
        self.answer_input.setAlignment(Qt.AlignCenter)
        # Only allow numbers to be entered
        self.answer_input.setValidator(QIntValidator())
        # Connect return key to submit answer
        self.answer_input.returnPressed.connect(self.submit_answer)
        
        # Create submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(SUBMIT_BUTTON_STYLE)
        self.submit_button.setMinimumHeight(50)
        self.submit_button.clicked.connect(self.submit_answer)
        
        # Add to layout - one row layout with input field and submit button
        self.answers_layout.addWidget(self.answer_input, 0, 0)
        self.answers_layout.addWidget(self.submit_button, 0, 1)

    def submit_answer(self) -> None:
        """Handle the submit button click in input mode."""
        # Get the answer from the input field
        text = self.answer_input.text()
        if text:
            try:
                answer = int(text)
                self.check_answer(answer)
            except ValueError:
                # If not a valid number, show error
                self.feedback_label.setText("Please enter a valid number")
                self.feedback_label.setStyleSheet(FEEDBACK_INCORRECT_STYLE)

    def check_answer(self, selected_answer: int) -> None:
        """Check if the selected answer is correct and update the UI accordingly.
        
        Args:
            selected_answer: The answer selected by the user
        """
        # Disable all answer inputs
        if self.input_mode:
            self.answer_input.setEnabled(False)
            self.submit_button.setEnabled(False)
        else:
            for i in range(self.answers_layout.count()):
                button = self.answers_layout.itemAt(i).widget()
                button.setEnabled(False)
        
        if selected_answer == self.expected_answer:
            self.correct_answers += 1
            self.show_correct_feedback()
        else:
            self.show_incorrect_feedback()
        
        # Update score indicator instead of text label
        self.score_indicator.set_score(self.correct_answers, self.total_questions, self.current_question)
        
        # Enable next button
        self.next_button.setEnabled(True)
        if self.current_question >= self.total_questions:
            self.next_button.setText(CORRECT_BUTTON_ICON)
        else:
            self.next_button.setText(NEXT_BUTTON_ICON)
    
    def show_correct_feedback(self) -> None:
        """Show feedback for a correct answer."""
        self.feedback_label.setText(CORRECT_FEEDBACK)
        self.feedback_label.setStyleSheet(FEEDBACK_CORRECT_STYLE)
        self.question_label.setText(self.format_question_with_answer())
        self.question_label.setStyleSheet(QUESTION_CORRECT_STYLE)
    
    def show_incorrect_feedback(self) -> None:
        """Show feedback for an incorrect answer."""
        self.feedback_label.setText(INCORRECT_FEEDBACK.format(self.expected_answer))
        self.feedback_label.setStyleSheet(FEEDBACK_INCORRECT_STYLE)
        self.question_label.setText(self.format_question_with_answer())
        self.question_label.setStyleSheet(QUESTION_INCORRECT_STYLE)

    def calculate_answer(self) -> int:
        """Calculate the correct answer based on the generated numbers.
        
        Returns:
            The correct answer for the current question
        
        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("Subclasses must implement calculate_answer")

    def format_question(self) -> str:
        """Format the question text.
        
        Returns:
            Formatted question text
            
        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("Subclasses must implement format_question")

    def format_question_with_answer(self) -> str:
        """Format the question text with the answer included.
        
        Returns:
            Formatted question text with answer
            
        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("Subclasses must implement format_question_with_answer")

    def set_total_questions(self, value):
        """Set the total number of questions in the quiz."""
        # Update the total questions property
        self.total_questions = value
        
        # Update the progress bar range
        self.progress_bar.setRange(0, value)
        
        # Update the label
        self.progress_label.setText(PROGRESS_LABEL_TEXT.format(self.current_question, self.total_questions))
        
        # If quiz is already in progress and we're now past the new total, show results
        if self.current_question > self.total_questions and not self.quiz_completed:
            self.show_results()

    def toggle_input_mode(self, state):
        """Toggle between button mode and input field mode.
        
        Args:
            state: Qt.CheckState value (0=unchecked, 2=checked)
        """
        # Convert Qt state to boolean (0=False, 2=True)
        self.input_mode = bool(state)
        
        # Regenerate the current question to update the UI
        # Store current question number
        current = self.current_question
        # Reset to regenerate
        self.current_question = current - 1
        self.generate_new_question() 

    def set_player_name(self, name: str) -> None:
        """Set the player name for score recording."""
        self.player_name = name if name else "Anonymous"

    def init_ui(self):
        """Initialize additional UI components and setup."""
        # Additional initialization logic if needed
        pass

    def next_question(self) -> None:
        """Show the next question in the quiz sequence or restart if completed."""
        print(f"DEBUG: next_question called, current_question before: {self.current_question}")
        
        # If this is the first question of a new quiz (current_question is 0)
        # Always set it to 1 (not incrementing)
        if self.current_question == 0:
            self.current_question = 1
            print(f"DEBUG: Set current_question to: {self.current_question}")
            # Update UI for question 1
            self.progress_bar.setValue(1)  
            print(f"DEBUG: Set progress bar to: 1")
            self.progress_label.setText(PROGRESS_LABEL_TEXT.format(1, self.total_questions))
            self.generate_new_question()
        else:
            # If we've already started, increment and generate
            self.generate_new_question()
        
        # Update score indicator
        self.score_indicator.set_score(self.correct_answers, self.total_questions, self.current_question)
        
        # Re-enable input for new question
        if self.input_mode:
            if hasattr(self, 'answer_input'):
                self.answer_input.setEnabled(True)
                self.answer_input.clear()
                self.answer_input.setFocus()
            if hasattr(self, 'submit_button'):
                self.submit_button.setEnabled(True)
        
        # Disable next button until an answer is submitted
        self.next_button.setEnabled(False)
        
        # Clear feedback label
        self.feedback_label.setText("") 