# Math Quiz Application

A modular, extensible math quiz application built with PySide6 (Qt for Python).

## Features

- Multiple quiz types (Addition, Multiplication)
- Visual aids for addition problems
- Responsive UI with modern styling
- Modular architecture for easy extension

## Project Structure

```
python-ui/
├── main.py                 # Main application entry point
├── quizzes/                # Quiz modules
│   ├── __init__.py         # Package initialization
│   ├── base_quiz.py        # Base quiz class with common functionality
│   ├── addition_quiz.py    # Addition quiz implementation
│   ├── multiplication_quiz.py # Multiplication quiz implementation
│   ├── components.py       # Reusable UI components
│   ├── styles.py           # Centralized styling
│   └── quiz_template.py    # Template for creating new quizzes
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Architecture

The application follows a modular architecture:

1. **BaseQuiz**: Abstract base class that provides common quiz functionality
2. **Specific Quiz Types**: Implementations for different types of quizzes
3. **Components**: Reusable UI components like dots, visual aids, and navigation
4. **Styles**: Centralized styling for consistent appearance

## Creating a New Quiz

To create a new quiz type:

1. Copy `quiz_template.py` to a new file (e.g., `subtraction_quiz.py`)
2. Rename the class and implement the required methods
3. Add the new quiz to `__init__.py`
4. Add a button for the new quiz in `main.py`

Example:

```python
# subtraction_quiz.py
from .base_quiz import BaseQuiz
from .components import NavigationBar

class SubtractionQuiz(BaseQuiz):
    """Quiz for practicing subtraction problems."""
    
    def __init__(self):
        super().__init__()
        self.nav_bar = NavigationBar(self.return_to_menu)
        self.layout.insertWidget(0, self.nav_bar)
    
    def return_to_menu(self):
        self.parent().parent().show_menu()
    
    def calculate_answer(self):
        return self.num1 - self.num2
    
    def format_question(self):
        return f"{self.num1} - {self.num2} = ?"
    
    def format_question_with_answer(self):
        return f"{self.num1} - {self.num2} = {self.correct_answer}"
```

## Styling

All styling is centralized in `styles.py`. To change the appearance of the application, modify the constants in this file.

## Dependencies

- PySide6 (Qt for Python)
- Python 3.6+

## Installation

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Development

For development, additional tools are available:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Format code
black .
isort .

# Check for linting issues
flake8
```
