# Math Quiz Application

A PySide6-based application for math quizzes targeting elementary school students.

## Features

- Multiple quiz types (addition, multiplication, etc.)
- Responsive UI that works across different screen sizes
- Customizable number of questions
- User management system
- Score tracking

## Project Structure

```
main.py                 (Entry point)
quizzes/                (Core package)
├── __init__.py         (Package initialization)
├── base_quiz.py        (Base quiz functionality)
├── components/         (UI components directory)
│   ├── __init__.py     (Components initialization)
│   ├── base_component.py (Base component class)
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
├── quiz_manager.py     (Quiz management singleton)
├── user_manager.py     (User management functionality)
├── database/           (Database functionality)
└── types/              (Quiz implementations)
    ├── __init__.py     (Quiz type exports)
    └── quiz_types.py   (Consolidated quiz implementations)
```

## Architecture

The application is designed with a modular architecture:

- `BaseQuiz`: Base class that all quizzes inherit from
- `BaseComponent`: Base class for UI components to standardize creation
- `Components`: Reusable UI components (TopBar, NavigationBar, ScoreIndicator)
- `QuizManager`: Centralized quiz registration and creation
- `UserManager`: Handles user-related functionality and state
- `QuizContainer`: Manages the active quiz and handles transitions
- `debug.py`: Centralized debug logging functionality
- `constants.py`: Centralized text strings for internationalization
- `mappings.py`: Configuration of menu items and quiz types

## Creating a New Quiz

Please refer to the `CREATING_QUIZZES.md` file for instructions on how to create new quiz types in the simplified structure. For legacy documentation, see `CreateQuiz.md` (deprecated).

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
pip install -r requirements-dev.txt

# Run linting
flake8
```

## Simplification

This project has undergone simplification to improve maintainability and reduce complexity:

1. Removed visual aid components
2. Consolidated quiz type implementations
3. Streamlined component architecture
4. Simplified quiz creation process

See `SIMPLIFICATIONS.md` for detailed information about these changes.
