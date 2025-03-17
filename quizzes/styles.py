"""
Centralized styling for the quiz application.
This module contains all the styles used in the application to make them easy to modify.
"""

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

# Label styles
QUESTION_LABEL_STYLE = "font-size: 24px; font-weight: bold;"
QUESTION_CORRECT_STYLE = "font-size: 24px; font-weight: bold; color: green;"
QUESTION_INCORRECT_STYLE = "font-size: 24px; font-weight: bold; color: red;"

FEEDBACK_LABEL_STYLE = "font-size: 18px;"
FEEDBACK_CORRECT_STYLE = "font-size: 18px; color: green;"
FEEDBACK_INCORRECT_STYLE = "font-size: 18px; color: red;"

EXPLANATION_LABEL_STYLE = "font-size: 16px; color: purple;"
NUMBER_LABEL_STYLE = "font-size: 16px;"

# Debug border styles (can be removed in production)
MAIN_BORDER_STYLE = "QWidget { border: 2px solid black; }"
NAV_BAR_BORDER_STYLE = "QWidget { border: 2px solid yellow; }"
VISUAL_AID_BORDER_STYLE = "QWidget { border: 2px solid red; }"
FIRST_GROUP_BORDER_STYLE = "QWidget { border: 2px solid green; }"
SECOND_GROUP_BORDER_STYLE = "QWidget { border: 2px solid orange; }"
DOTS_CONTAINER_BORDER_STYLE = "QWidget { border: 2px solid purple; }"

# Colors
BLUE_DOT_COLOR = (0, 0, 255)  # RGB for blue dots
RED_DOT_COLOR = (255, 0, 0)   # RGB for red dots
YELLOW_DOT_COLOR = (255, 255, 0)  # RGB for highlighted dots

# Layout settings
DEFAULT_SPACING = 10
BUTTON_SPACING = 15
DOTS_ROW_SIZE = 5  # Number of dots per row 