"""
Centralized styling for the quiz application.
This module contains all the styles used in the application to make them easy to modify.
"""

# Debug mode - set to True to show borders during development
DEBUG_MODE = False

# Window settings
WINDOW_TITLE = "Math Quiz"
WINDOW_INITIAL_POSITION = (100, 100)
WINDOW_INITIAL_SIZE = (800, 600)
WINDOW_MINIMUM_SIZE = (600, 400)

# Button styles
ANSWER_BUTTON_STYLE = """
    QPushButton {
        background-color: #4a86e8;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #2d5bb9;
    }
    QPushButton:hover {
        background-color: #2d5bb9;
    }
    QPushButton:pressed {
        background-color: #1c3a75;
    }
"""

NEXT_BUTTON_STYLE = """
    QPushButton {
        background-color: #FF9800;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #F57C00;
    }
    QPushButton:hover {
        background-color: #F57C00;
    }
    QPushButton:pressed {
        background-color: #E65100;
    }
"""

RETURN_BUTTON_STYLE = """
    QPushButton {
        background-color: #f44336;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: 1px solid #ba000d;
    }
    QPushButton:hover {
        background-color: #ba000d;
    }
"""

SHOW_HINT_BUTTON_STYLE = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #388E3C;
    }
    QPushButton:hover {
        background-color: #388E3C;
    }
    QPushButton:pressed {
        background-color: #1B5E20;
    }
"""

MENU_BUTTON_STYLE = """
    QPushButton {
        background-color: #2196F3;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #0D47A1;
    }
    QPushButton:hover {
        background-color: #1976D2;
    }
    QPushButton:pressed {
        background-color: #0D47A1;
    }
"""

# Label styles
QUESTION_LABEL_STYLE = "font-size: 28px; font-weight: bold;"
QUESTION_CORRECT_STYLE = "font-size: 24px; font-weight: bold; color: green;"
QUESTION_INCORRECT_STYLE = "font-size: 24px; font-weight: bold; color: red;"

FEEDBACK_LABEL_STYLE = "font-size: 18px;"
FEEDBACK_CORRECT_STYLE = "font-size: 18px; color: green;"
FEEDBACK_INCORRECT_STYLE = "font-size: 18px; color: red;"

EXPLANATION_LABEL_STYLE = "font-size: 16px; color: white;"
NUMBER_LABEL_STYLE = "font-size: 18px;"

# Debug border styles (toggled based on DEBUG_MODE)
MAIN_BORDER_STYLE = "QWidget { border: 2px solid black; }" if DEBUG_MODE else ""
NAV_BAR_BORDER_STYLE = "QWidget { border: 2px solid yellow; }" if DEBUG_MODE else ""
VISUAL_AID_BORDER_STYLE = "QWidget { border: 2px solid red; }" if DEBUG_MODE else ""
FIRST_GROUP_BORDER_STYLE = "QWidget { border: 2px solid green; }" if DEBUG_MODE else ""
SECOND_GROUP_BORDER_STYLE = "QWidget { border: 2px solid orange; }" if DEBUG_MODE else ""
DOTS_CONTAINER_BORDER_STYLE = "QWidget { border: 2px solid purple; }" if DEBUG_MODE else ""

# Additional debug borders for other main containers
MENU_CONTAINER_BORDER_STYLE = "QWidget { border: 2px solid blue; }" if DEBUG_MODE else ""
QUIZ_CONTAINER_BORDER_STYLE = "QWidget { border: 2px solid red; }" if DEBUG_MODE else ""
ANSWERS_CONTAINER_BORDER_STYLE = "QWidget { border: 2px solid green; }" if DEBUG_MODE else ""

# Colors
BLUE_DOT_COLOR = (0, 0, 255)  # RGB for blue dots
RED_DOT_COLOR = (255, 0, 0)   # RGB for red dots
YELLOW_DOT_COLOR = (255, 255, 0)  # RGB for highlighted dots
SCORE_GOOD_COLOR = (80, 200, 120)  # RGB for good score (green)
SCORE_BAD_COLOR = (220, 70, 70)    # RGB for bad score (red)

# Layout settings
DEFAULT_SPACING = 10
BUTTON_SPACING = 15
DOTS_ROW_SIZE = 5  # Number of dots per row

# Main window layout
MAIN_LAYOUT_MARGINS = (10, 10, 10, 10)  # Left, Top, Right, Bottom
MAIN_LAYOUT_SPACING = 20

# Menu layout
MENU_LAYOUT_SPACING = 20
MENU_BUTTON_SIZE = (200, 120)  # Minimum width, height

# Quiz layout
QUIZ_LAYOUT_SPACING = 20
QUIZ_LAYOUT_MARGINS = (0, 0, 0, 0)  # Left, Top, Right, Bottom

# Answers layout
ANSWERS_LAYOUT_SPACING = 10
ANSWER_BUTTON_SIZE = (200, 50)  # Minimum width, height

# Fixed height values
VISUAL_AID_HEIGHT = 190  # Fixed height for visual aid container and widget
NAV_BAR_HEIGHT = 40  # Fixed height for navigation bar

# Quiz options
DEFAULT_QUIZ_QUESTIONS = 20  # Default number of questions in a quiz

# Text strings
CORRECT_FEEDBACK = "Super! Dobra robota!"
INCORRECT_FEEDBACK = "Nie! Poprawna odpowiedź to {}"

# Menu items
MENU_ITEMS = [
    "Mnożenie 2-5",
    "Dodawanie do 20",
    "Mnożenie małych liczb",
    "Odejmowanie",
    "Item 5", 
    "Item 6"
]

# Quiz type mapping
QUIZ_TYPE_MAP = {
    "Mnożenie 2-5": "MultiplicationQuiz",
    "Dodawanie do 20": "AdditionQuiz",
    "Mnożenie małych liczb": "SmallMultiplicationQuiz",
    "Odejmowanie": "SubtractionQuiz"
}

# Score box styles
SCORE_BOX_WIDTH = 60 
SCORE_BOX_HEIGHT = 18
SCORE_BOX_STYLE = """
    border: 1px solid #888;
    border-radius: 4px;
    background-color: #f0f0f0;
""" 