# Creating New Quizzes

This guide explains how to create new quiz types for the math quiz application.

## Architecture Overview

The quiz application uses a modular architecture with these key components:

1. **BaseQuiz** - The foundation class for all quizzes
2. **Quiz factory function** - For creating custom quizzes with minimal code
3. **Components** - Reusable UI components like NavigationBar, TopBar, etc.
4. **Visual aids** - Optional components to help visualize math problems

## Project Structure

The quiz application uses the following structure:

```
quizzes/                  (Core package)
├── __init__.py           (Main package initialization)
├── base_quiz.py          (Base quiz functionality)
├── components/           (UI components directory)
│   ├── __init__.py       (Components initialization)
│   ├── navigation_bar.py (Navigation bar component)
│   ├── top_bar.py        (Top bar component)
│   └── score_indicator.py (Score indicator component)
├── debug.py              (Debug logging utilities)
├── styles.py             (UI styling and colors)
├── constants.py          (String constants for UI text)
├── mappings.py           (Menu items and quiz type mappings)
├── menu.py               (Menu component)
├── quiz_container.py     (Quiz container component)
├── create_quiz_factory.py (Factory function for creating quizzes)
├── user_manager.py       (User management functionality)
└── types/                (Subfolder for quiz implementations)
    ├── __init__.py       (Exports all quiz classes)
    ├── addition_quiz.py  (Addition quiz implementation)
    ├── multiplication_quiz.py (Multiplication quiz)
    └── custom_quizzes.py (Factory-created quizzes)
```

When creating a new quiz, place your implementation in the `quizzes/types/` directory to keep the codebase organized.

## Creating a New Quiz

You have two main approaches for creating quizzes:

### Approach 1: Using the Factory Function (Recommended)

Create a new file in the `quizzes/types/` directory:

```python
# quizzes/types/my_new_quiz.py
import random
from quizzes import create_custom_quiz

def create_my_new_quiz(total_questions=15):
    """Create a new custom quiz."""
    
    def generate_numbers(quiz):
        """Generate numbers for this quiz."""
        quiz.num1 = random.randint(1, 10)  # Set first number
        quiz.num2 = random.randint(1, 10)  # Set second number
    
    def calculate_answer(quiz):
        """Calculate the answer based on numbers."""
        return quiz.num1 + quiz.num2  # For addition quiz
    
    def format_question(quiz):
        """Format the question text."""
        return f"{quiz.num1} + {quiz.num2} = ?"
    
    # Create and return the quiz class
    return create_custom_quiz(
        name="My New Quiz",
        number_generator=generate_numbers,
        answer_calculator=calculate_answer,
        question_formatter=format_question,
        visual_aid_class=None,  # Optional visual aid class
        total_questions=total_questions
    )

# Create the quiz class
MyNewQuiz = create_my_new_quiz()
```

Then register it in `quizzes/mappings.py`:

```python
# Add to MENU_ITEMS
MENU_ITEMS = [
    "Mnożenie 2-5",
    "Dodawanie do 20",
    "Mnożenie małych liczb",
    "Odejmowanie od 10-20",
    "My New Quiz",  # Add your quiz name
    "Item 6"
]

# Add to QUIZ_TYPE_MAP
QUIZ_TYPE_MAP = {
    "Mnożenie 2-5": "MultiplicationQuiz",
    "Dodawanie do 20": "AdditionQuiz",
    "Mnożenie małych liczb": "SmallMultiplicationQuiz",
    "Odejmowanie od 10-20": "SubtractionQuiz",
    "My New Quiz": "MyNewQuiz"  # Map name to class
}
```

Finally, import and export your quiz in `quizzes/types/__init__.py`:

```python
from .addition_quiz import AdditionQuiz
from .multiplication_quiz import MultiplicationQuiz
from .custom_quizzes import SmallMultiplicationQuiz, SubtractionQuiz
from .my_new_quiz import MyNewQuiz

__all__ = [
    'AdditionQuiz',
    'MultiplicationQuiz',
    'SmallMultiplicationQuiz',
    'SubtractionQuiz',
    'MyNewQuiz'
]
```

And update the main `quizzes/__init__.py` to import from the types directory:

```python
from .types import MyNewQuiz  # Add your new quiz here
```

### Approach 2: Creating a Subclass of BaseQuiz

For more customization, create a file in the types directory:

```python
# quizzes/types/my_custom_quiz.py
import random
from quizzes.base_quiz import BaseQuiz
from quizzes.components import NavigationBar

class MyCustomQuiz(BaseQuiz):
    """A more customized quiz implementation."""
    
    def __init__(self, total_questions=20, show_questions_control=True):
        """Initialize the quiz."""
        super().__init__(total_questions=total_questions)
        
        # Add navigation bar
        self.nav_bar = NavigationBar(self.return_to_menu)
        
        # Add questions control if requested
        if show_questions_control:
            self.questions_spinbox = self.nav_bar.add_questions_spinbox(
                initial_value=total_questions,
                callback=self.update_total_questions
            )
        
        # Add any additional components
        # ...
        
        # Add the navigation bar to the top of the layout
        self.layout.insertWidget(0, self.nav_bar)
    
    def generate_numbers(self):
        """Generate numbers for this quiz."""
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
    
    def calculate_answer(self):
        """Calculate the answer for the current question."""
        return self.num1 * self.num2
    
    def format_question(self):
        """Format the question text."""
        return f"{self.num1} × {self.num2} = ?"
    
    def format_question_with_answer(self):
        """Format the question with the answer included."""
        return f"{self.num1} × {self.num2} = {self.correct_answer}"
```

## Adding a Visual Aid to Your Quiz

Visual aids help students visualize math concepts. To add one:

1. Create a visual aid class:

```python
from quizzes.components import VisualAidWidget

class MyVisualAid(VisualAidWidget):
    """Custom visual aid for a quiz."""
    
    def __init__(self, num1, num2):
        super().__init__(num1, num2)
        # Setup your visual representation
        # ...
    
    def paintEvent(self, event):
        """Custom paint method to draw your visual aid."""
        super().paintEvent(event)
        painter = QPainter(self)
        # Draw your visual representation
        # ...
```

2. Add it to your quiz (factory approach):

```python
return create_custom_quiz(
    name="My New Quiz",
    number_generator=generate_numbers,
    answer_calculator=calculate_answer,
    question_formatter=format_question,
    visual_aid_class=MyVisualAid,  # Use your visual aid class
    total_questions=total_questions
)
```

3. Or add it to your custom quiz class:

```python
def __init__(self, total_questions=20, show_questions_control=True):
    # ... existing code ...
    
    # Add visual aid
    self.setup_visual_aid(MyVisualAid)
```

## Method Overrides in Custom Quizzes

The BaseQuiz class provides these methods you can override:

| Method | Purpose | Required? |
|--------|---------|-----------|
| `generate_numbers()` | Set `self.num1` and `self.num2` | Yes |
| `calculate_answer()` | Return the correct answer | Yes |
| `format_question()` | Return question text | Yes |
| `format_question_with_answer()` | Question with answer | Yes |
| `on_new_question()` | Called when a new question starts | No |
| `check_answer()` | Custom answer checking logic | No |
| `show_results()` | Custom results screen | No |

## Complete Examples

For complete examples, look at:

1. `quizzes/types/addition_quiz.py` - Full class implementation
2. `quizzes/types/custom_quizzes.py` - Factory-created quizzes

## Styling Your Quiz

All visual styles are defined in `quizzes/styles.py`, while text constants are in `quizzes/constants.py` and menu configuration is in `quizzes/mappings.py`. You can:

1. Use existing styles and constants
2. Add new styles for your quiz
3. Add new strings to constants.py if needed
4. Register your quiz in mappings.py

## Using Text Constants

For better organization and to support potential internationalization, all user-facing text strings should be defined in `constants.py`. For example:

```python
# In quizzes/constants.py
MY_QUIZ_CORRECT_MESSAGE = "Great job solving the equation!"
MY_QUIZ_TOOLTIP = "Try the new quiz type"
```

Then use these constants in your quiz implementation:

```python
from quizzes.constants import MY_QUIZ_CORRECT_MESSAGE, MY_QUIZ_TOOLTIP

class MyCustomQuiz(BaseQuiz):
    # ...
    
    def show_correct_feedback(self):
        self.feedback_label.setText(MY_QUIZ_CORRECT_MESSAGE)
        self.feedback_label.setStyleSheet(FEEDBACK_CORRECT_STYLE)
        self.feedback_label.show()
```

## Best Practices

1. **Keep number generation logic simple** but appropriate for the quiz type
2. **Test your quiz with edge cases** (zeros, negative numbers, etc.)
3. **Use visual aids when appropriate** to help students understand concepts
4. **Follow existing code patterns** for consistency
5. **Add your quiz to mappings.py** to make it appear in the menu
6. **Define strings in constants.py** for better organization 