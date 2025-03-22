"""
File-based quiz module for loading quizzes from external files.

This module allows creating quizzes from JSON files containing question-answer pairs
without requiring any coding.
"""
import json
import os
import random
from typing import List, Dict, Any, Optional, Union

from .base_quiz import BaseQuiz
from .components.navigation_bar import NavigationBar
from .debug import log

class FileBasedQuiz(BaseQuiz):
    """Quiz that loads questions and answers from a JSON file."""
    
    def __init__(
        self, 
        file_path: str, 
        parent=None, 
        total_questions=None, 
        show_questions_control=True, 
        input_mode="self_assess",
        shuffle=True
    ):
        """Initialize a file-based quiz.
        
        Args:
            file_path: Path to the JSON file containing questions and answers
            parent: Parent widget
            total_questions: Maximum number of questions to use (or None for all)
            show_questions_control: Whether to show questions count control
            input_mode: Input mode (self_assess, True for input field, False for buttons)
            shuffle: Whether to shuffle the questions
        """
        self.file_path = file_path
        self.questions = self._load_questions(file_path, shuffle)
        
        # Set total questions based on file content if not specified
        if total_questions is None or total_questions > len(self.questions):
            total_questions = len(self.questions)
        
        # Call parent constructor
        super().__init__(
            parent=parent,
            total_questions=total_questions,
            show_questions_control=show_questions_control,
            input_mode=input_mode
        )
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        
        # Add input mode toggle only if input mode is not fixed
        if input_mode is None:
            self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
                checked=False,
                callback=self.toggle_input_mode
            )
        
        # Add spinbox for number of questions if enabled
        if show_questions_control:
            # Limit max questions to available questions
            self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                initial_value=total_questions,
                callback=self.set_total_questions,
                maximum=len(self.questions)
            )
        
        self.main_layout.insertWidget(0, self.nav_bar)
        
        # Current question index
        self.current_index = -1  # Will be incremented in generate_numbers
    
    def _load_questions(self, file_path: str, shuffle: bool) -> List[Dict[str, Any]]:
        """Load questions from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            shuffle: Whether to shuffle the questions
            
        Returns:
            List of question dictionaries
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            
            # Validate structure
            for i, q in enumerate(questions):
                if 'question' not in q:
                    raise ValueError(f"Question {i+1} is missing 'question' field")
                if 'answer' not in q:
                    raise ValueError(f"Question {i+1} is missing 'answer' field")
            
            # Shuffle questions if requested
            if shuffle:
                random.shuffle(questions)
                
            return questions
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log("FileBasedQuiz", f"Error loading questions from {file_path}: {e}")
            # Return an error question to make the quiz still functional
            return [{"question": f"Error loading questions: {e}", "answer": ""}]
    
    def generate_numbers(self) -> None:
        """Get the next question from the loaded questions."""
        # Increment the current index, wrapping around if needed
        self.current_index = (self.current_index + 1) % len(self.questions)
        
        # Store the current question and answer
        current_question = self.questions[self.current_index]
        self.current_question_text = current_question['question']
        self.expected_answer = current_question['answer']
        
        # Placeholder values for num1/num2 (not used but required by BaseQuiz)
        self.num1 = 0
        self.num2 = 0
    
    def calculate_answer(self) -> Union[int, str]:
        """Return the answer for the current question."""
        return self.expected_answer
    
    def format_question(self) -> str:
        """Format the question text."""
        return self.current_question_text
    
    def format_question_with_answer(self) -> str:
        """Format the question with the answer included."""
        return f"{self.current_question_text}\nAnswer: {self.expected_answer}"

    def generate_answer_options(self) -> List[Union[int, str]]:
        """Generate answer options for the question.
        
        For file-based quizzes, we need to handle both numeric and text answers.
        
        Returns:
            List of possible answers including the correct one
        """
        # Try to convert the answer to an integer if it's numeric
        try:
            # If the answer is a number, generate numeric options
            answer_value = int(self.expected_answer)
            
            # Generate options around the correct answer if it's a number
            options = []
            while len(options) < 3:
                # Generate options within a reasonable range of the answer
                option = random.randint(max(1, answer_value - 10), answer_value + 10)
                if option != answer_value and option not in options:
                    options.append(option)
            
            # Add the correct answer and shuffle
            options.append(answer_value)
            random.shuffle(options)
            return options
        
        except (ValueError, TypeError):
            # For text answers, we don't generate alternatives
            # Just return the correct answer, which will trigger input mode
            # regardless of the setting
            return [self.expected_answer]


def create_quiz_from_file(file_path: str, quiz_name: Optional[str] = None, input_mode: Optional[Union[bool, str]] = None) -> FileBasedQuiz:
    """Factory function to create a quiz from a file.
    
    Args:
        file_path: Path to the JSON file with questions
        quiz_name: Name for the quiz (or None to use filename)
        input_mode: If provided, sets the input mode for the quiz:
                   - True: use input field mode
                   - False: use buttons mode
                   - "self_assess": use self-assessment mode
                   - None: use default (self-assessment mode)
        
    Returns:
        A FileBasedQuiz subclass
    """
    # Use file name as quiz name if not provided
    if quiz_name is None:
        quiz_name = os.path.splitext(os.path.basename(file_path))[0]
    
    class CustomFileQuiz(FileBasedQuiz):
        """Custom file-based quiz."""
        
        def __init__(self, parent=None, total_questions=None, show_questions_control=True, input_mode=input_mode):
            """Initialize with the specified file."""
            # Set default input mode if none provided
            if input_mode is None:
                input_mode = "self_assess"
            
            # Initialize necessary attributes before the parent constructor is called
            self.file_path = file_path
            self.questions = self._load_questions(file_path, True)  # Default to shuffle=True
            self.current_index = -1  # Initialize current_index before calling parent.__init__
            
            # If total_questions is None or greater than available questions, adjust it
            if total_questions is None or total_questions > len(self.questions):
                total_questions = len(self.questions)
            
            # Now call the parent constructor with pre-initialized attributes
            BaseQuiz.__init__(
                self,
                parent=parent,
                total_questions=total_questions,
                show_questions_control=show_questions_control,
                input_mode=input_mode
            )
            
            # Set the quiz name
            self.quiz_name = quiz_name
            
            # Add navigation bar
            self.nav_bar = NavigationBar(self.return_to_menu)
            
            # Add input mode toggle only if input mode is not fixed
            if input_mode is None:
                self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
                    checked=False,
                    callback=self.toggle_input_mode
                )
            
            # Add spinbox for number of questions if enabled
            if show_questions_control:
                # Limit max questions to available questions
                self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                    initial_value=total_questions,
                    callback=self.set_total_questions,
                    maximum=len(self.questions)
                )
            
            self.main_layout.insertWidget(0, self.nav_bar)
        
        def check_answer(self, user_answer):
            """Check if the answer is correct, with normalization for different formats.
            
            Args:
                user_answer: The user's answer (str or int)
                
            Returns:
                True if correct, False otherwise
            """
            # Convert both to strings and strip whitespace for case-insensitive comparison
            expected = str(self.expected_answer).strip().lower()
            given = str(user_answer).strip().lower()
            
            return expected == given
    
    return CustomFileQuiz 