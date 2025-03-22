# Creating Quizzes - Simplified Guide

This guide explains how to create new quiz types in the simplified architecture.

## Overview

The quiz application now uses a simplified architecture that:

1. Eliminates visual aids for cleaner code
2. Consolidates quiz types in a single file
3. Provides multiple methods to create quizzes with different levels of abstraction

## Project Structure

```
quizzes/
├── components/         (UI components)
├── types/
│   ├── __init__.py     (Exports quiz classes)
│   └── quiz_types.py   (All quiz implementations)
├── base_quiz.py        (Base quiz class)
├── create_quiz_factory.py (Quiz factory function)
└── quiz_manager.py     (Quiz management singleton)
```

## Creating a New Quiz

You have three approaches to creating a new quiz:

### Option 1: Direct BaseQuiz Subclass

Create your quiz by subclassing BaseQuiz directly for maximum flexibility:

```python
# In quizzes/types/quiz_types.py

import random
from ..base_quiz import BaseQuiz
from ..components import NavigationBar

class MyNewQuiz(BaseQuiz):
    def __init__(self, parent=None, total_questions=10, show_questions_control=True):
        super().__init__(
            parent=parent,
            total_questions=total_questions,
            show_questions_control=show_questions_control
        )
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        
        # Add input mode toggle
        self.input_mode_toggle = self.nav_bar.add_input_mode_toggle(
            checked=False,
            callback=self.toggle_input_mode
        )
        
        # Add questions control if needed
        if show_questions_control:
            self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                initial_value=total_questions,
                callback=self.set_total_questions
            )
        
        self.main_layout.insertWidget(0, self.nav_bar)
    
    def generate_numbers(self):
        """Generate your question numbers here."""
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
    
    def calculate_answer(self):
        """Calculate the expected answer."""
        return self.num1 + self.num2
    
    def format_question(self):
        """Format how the question appears to the user."""
        return f"{self.num1} + {self.num2} = ?"
    
    def format_question_with_answer(self):
        """Format how the answered question appears."""
        return f"{self.num1} + {self.num2} = {self.expected_answer}"
```

### Option 2: Using the Factory Function

Define your quiz using the `create_custom_quiz` factory function for simpler creation:

```python
# In quizzes/types/quiz_types.py or in a new file

from ..create_quiz_factory import create_custom_quiz
import random

def create_my_new_quiz():
    """Create a custom quiz type."""
    
    def generate_numbers(quiz):
        quiz.num1 = random.randint(1, 10)
        quiz.num2 = random.randint(1, 10)
    
    def calculate_answer(quiz):
        return quiz.num1 + quiz.num2
    
    def format_question(quiz):
        return f"{quiz.num1} + {quiz.num2} = ?"
    
    return create_custom_quiz(
        name="My New Quiz",
        number_generator=generate_numbers,
        answer_calculator=calculate_answer,
        question_formatter=format_question,
        total_questions=15
    )

# Create an instance of your quiz class
MyNewQuiz = create_my_new_quiz()
```

### Option 3: Using the Quiz Manager

Register your quiz with the central QuizManager:

```python
# In quizzes/types/quiz_types.py or another file

from ..quiz_manager import quiz_manager
from ..base_quiz import BaseQuiz

class MyNewQuiz(BaseQuiz):
    # Quiz implementation...
    pass

# Register the quiz
quiz_manager.create_simple_quiz("MyNewQuiz", MyNewQuiz)

# Later, create an instance
quiz = quiz_manager.create_quiz("MyNewQuiz", total_questions=10)
```

## Adding Your Quiz to the Menu

Update the `QUIZ_TYPE_MAP` in `quizzes/mappings.py`:

```python
QUIZ_TYPE_MAP = {
    "My New Quiz": "MyNewQuiz",
    # ... other mappings
}
```

## Quiz BaseClass Features

The BaseQuiz provides core features that every quiz inherits:

- Question generation
- Score tracking
- User interaction handling (buttons or text input)
- Feedback for correct/incorrect answers
- Progress tracking

Your quiz must implement these methods:

- `generate_numbers()` - Set up the num1 and num2 values
- `calculate_answer()` - Return the expected answer
- `format_question()` - Format the question display text
- `format_question_with_answer()` - Format for review screen

## Navigation Bar Features

The NavigationBar component provides these features:

- Back button for returning to the menu
- Optional input mode toggle
- Optional question count spinner
- Other control elements as needed

## Tips for Creating Effective Quizzes

1. **Clear Questions**: Ensure questions are formatted clearly
2. **Consistent Difficulty**: Keep question difficulty appropriate
3. **Meaningful Feedback**: Provide helpful feedback on answers
4. **Randomization**: Ensure good variety in the questions
5. **Error Handling**: Validate user input properly

## Testing Your Quiz

Run the application and navigate to your quiz from the menu:

```bash
python main.py
``` 