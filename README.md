# Math Quiz Application

A PySide6-based application for math quizzes targeting elementary school students.

## Features

- Multiple quiz types (addition, multiplication, etc.)
- Visual aids to help understand concepts
- Responsive UI that works across different screen sizes
- Customizable number of questions

## Project Structure

```
main.py                 (Entry point)
quizzes/                (Core package)
├── __init__.py         (Package initialization)
├── base_quiz.py        (Base quiz functionality)
├── components/         (UI components directory)
│   ├── __init__.py     (Components initialization)
│   ├── navigation_bar.py (Navigation bar component)
│   ├── top_bar.py      (Top bar component)
│   └── score_indicator.py (Score indicator component)
├── debug.py            (Debug logging utilities)
├── styles.py           (UI styling and colors)
├── constants.py        (String constants)
├── mappings.py         (Menu and quiz type mappings)
├── menu.py             (Menu component)
├── quiz_container.py   (Quiz container component)
├── create_quiz_factory.py (Factory for creating quizzes)
├── user_manager.py     (User management functionality)
└── types/              (Quiz implementations)
    ├── addition_quiz.py
    ├── multiplication_quiz.py
    └── custom_quizzes.py
requirements.txt        (Dependencies)
```

## Architecture

The application is designed with a modular architecture:

- `BaseQuiz`: Abstract base class that all quizzes inherit from
- `Components`: Reusable UI components (TopBar, NavigationBar, ScoreIndicator)
- `UserManager`: Handles user-related functionality and state
- `QuizContainer`: Manages the active quiz and handles transitions
- `debug.py`: Centralized debug logging functionality
- `constants.py`: Centralized text strings for internationalization
- `mappings.py`: Configuration of menu items and quiz types

## Creating a New Quiz

Please refer to the `CreateQuiz.md` file for detailed instructions on how to create new quiz types.

## Debugging

The application includes a debug logging system. To enable it, run:

```bash
python main.py --debug
```

This will display detailed logging information during application execution.

## Styling

All styles are centralized in `styles.py`, making it easy to adjust the look and feel of the application.

## Dependencies

- PySide6 (Qt for Python)
- Python 3.6+

## Installation

```bash
# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Development

```bash
# Install development dependencies
pip install -r dev-requirements.txt

# Run linting
flake8
```
