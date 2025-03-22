"""
File-based quiz module for loading quizzes from external files.

This module allows creating quizzes from JSON files containing question-answer pairs
without requiring any coding.
"""
import json
import os
import random
from typing import List, Dict, Any, Optional, Union

from ..base_quiz import BaseQuiz
from ..components.navigation_bar import NavigationBar
from ..debug import log

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
            file_path: Path to the JSON file with questions
            parent: Parent widget
            total_questions: Number of questions to ask
            show_questions_control: Whether to show the questions control
            input_mode: Mode of input ('self_assess', 'buttons', or 'input')
            shuffle: Whether to shuffle the questions
        """
        # We'll initialize these before super().__init__ so they are available in generate_numbers
        self.questions = []
        self.current_index = 0
        self.file_path = file_path
        self.current_question_text = ""
        self.current_answer_text = ""
        self.options = []
        
        # Load questions from file
        self.questions = self._load_questions(file_path, shuffle)
        
        # Determine total questions (cap by available questions)
        if total_questions is None or total_questions > len(self.questions):
            actual_total = len(self.questions)
        else:
            actual_total = min(total_questions, len(self.questions))
        
        BaseQuiz.__init__(
            self,
            parent=parent,
            total_questions=actual_total,
            show_questions_control=show_questions_control,
            input_mode=input_mode
        )
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        
        # Add input mode toggle
        self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
            checked=input_mode == "input",
            callback=self.toggle_input_mode
        )
        
        # Insert nav bar at the top
        self.main_layout.insertWidget(0, self.nav_bar)
    
    def _load_questions(self, file_path: str, shuffle: bool) -> List[Dict[str, Any]]:
        """Load questions from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            shuffle: Whether to shuffle the questions
            
        Returns:
            List of question dictionaries
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check if data is a dictionary with 'questions' key
            if isinstance(data, dict) and 'questions' in data:
                questions = data['questions']
            elif isinstance(data, list):
                questions = data
            else:
                log("FileBasedQuiz", f"Invalid data format in {file_path}")
                questions = []
                
            # Apply shuffle if requested
            if shuffle and questions:
                random.shuffle(questions)
                
            return questions
        except Exception as e:
            log("FileBasedQuiz", f"Error loading questions from {file_path}: {str(e)}")
            return []
    
    def generate_numbers(self) -> None:
        """Get the next question from the loaded questions."""
        if not self.questions or self.current_index >= len(self.questions):
            self.current_question_text = "No more questions"
            self.current_answer_text = ""
            self.options = []
            return
            
        current_item = self.questions[self.current_index]
        self.current_question_text = current_item.get('question', '')
        self.current_answer_text = current_item.get('answer', '')
        self.options = current_item.get('options', [])
        self.current_index += 1
    
    def calculate_answer(self) -> Union[int, str]:
        """Return the answer for the current question."""
        return self.current_answer_text
    
    def format_question(self) -> str:
        """Format the current question text."""
        return self.current_question_text
    
    def format_question_with_answer(self) -> str:
        """Format the question text with the answer included."""
        return f"{self.current_question_text}\nAnswer: {self.current_answer_text}"
    
    def generate_answer_options(self) -> List[Union[int, str]]:
        """Generate answer options for the current question.
        
        This method will use any provided options in the question data.
        If no options are provided, it falls back to the base implementation.
        
        Returns:
            List of answer options
        """
        if self.options:
            # If the correct answer is not in options, add it
            if self.current_answer_text not in self.options:
                options = self.options + [self.current_answer_text]
                # Shuffle to avoid correct answer always being last
                random.shuffle(options)
                return options
            return self.options
        else:
            # No options provided in the question, use base implementation
            # For text-based answers, we'll need to provide plausible alternatives
            # This is challenging without additional context
            # For now, we'll return just the correct answer for button mode
            return [self.current_answer_text]


def create_quiz_from_file(file_path: str, quiz_name: Optional[str] = None, input_mode: Optional[Union[bool, str]] = None) -> FileBasedQuiz:
    """Create a quiz from a JSON file.
    
    This function creates a specialized FileBasedQuiz class for the given file,
    which can be registered with the quiz manager.
    
    Args:
        file_path: Path to the JSON file
        quiz_name: Optional name for the quiz class
        input_mode: Input mode for the quiz ('buttons', 'input', or 'self_assess')
                    If True, uses 'input', if False uses 'self_assess'
    
    Returns:
        A FileBasedQuiz subclass
    """
    # Normalize input_mode
    if input_mode is True:
        input_mode = 'input'
    elif input_mode is False:
        input_mode = 'self_assess'
    
    # Create a custom quiz class
    class CustomFileQuiz(FileBasedQuiz):
        """Custom quiz class for a specific file."""
        
        def __init__(self, parent=None, total_questions=None, show_questions_control=True, input_mode=input_mode):
            """Initialize the custom file quiz.
            
            Args:
                parent: Parent widget
                total_questions: Number of questions to ask
                show_questions_control: Whether to show the questions control
                input_mode: Mode of input ('self_assess', 'buttons', or 'input')
            """
            # Load file and get quiz metadata if available
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Extract quiz metadata if available
                if isinstance(data, dict):
                    metadata = data.get('metadata', {})
                    # Determine final input mode, with precedence:
                    # 1. Parameter passed to create_quiz_from_file
                    # 2. Metadata in JSON file
                    # 3. Default ('self_assess')
                    file_input_mode = metadata.get('input_mode')
                    actual_input_mode = input_mode or file_input_mode or 'self_assess'
                    
                else:
                    actual_input_mode = input_mode or 'self_assess'
            except Exception:
                actual_input_mode = input_mode or 'self_assess'
            
            super().__init__(
                file_path=file_path,
                parent=parent,
                total_questions=total_questions,
                show_questions_control=show_questions_control,
                input_mode=actual_input_mode
            )
        
        def check_answer(self, user_answer):
            """Check if the answer is correct, with special handling for multiple correct answers.
            
            Args:
                user_answer: The user's answer
            
            Returns:
                Whether the answer is correct
            """
            # Get current question
            if not self.questions or self.current_index <= 0 or self.current_index > len(self.questions):
                return False
                
            current_item = self.questions[self.current_index - 1]
            
            # Check for multiple correct answers
            correct_answers = current_item.get('correct_answers', [])
            if correct_answers:
                # Convert answers to strings for comparison
                correct_answers = [str(ans).strip().lower() for ans in correct_answers]
                user_answer_str = str(user_answer).strip().lower()
                return user_answer_str in correct_answers
            else:
                # Fall back to the standard answer
                correct_answer = str(self.current_answer_text).strip().lower()
                user_answer_str = str(user_answer).strip().lower()
                return user_answer_str == correct_answer
    
    # Set the class name if provided
    if quiz_name:
        CustomFileQuiz.__name__ = quiz_name
    else:
        # Generate a name based on the file name
        base_name = os.path.basename(file_path)
        name_parts = os.path.splitext(base_name)[0].split('_')
        class_name = ''.join(part.capitalize() for part in name_parts) + 'Quiz'
        CustomFileQuiz.__name__ = class_name
    
    return CustomFileQuiz 