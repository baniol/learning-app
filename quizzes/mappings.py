"""
Mapping constants for the quiz application.
This module contains all mapping dictionaries and lists used for configuration.
"""

# Main menu categories
MENU_CATEGORIES = [
    "Math",
    "Languages",
    "Settings",
    "Stats"
]

# Submenu items for each category
SUBMENU_ITEMS = {
    "Math": [
        "Mnożenie 2-5",
        "Dodawanie do 20",
        "Mnożenie małych liczb",
        "Odejmowanie od 10-20"
    ],
    "Languages": [
        "English Words",
        "Spanish Words",
    ],
    "Settings": [
        "Preferences",
        "Themes",
    ],
    "Stats": [
        "Progress",
        "History",
        "Scores"
    ]
}

# Maps menu item names to quiz class names
QUIZ_TYPE_MAP = {
    "Mnożenie 2-5": "MultiplicationQuiz",
    "Dodawanie do 20": "AdditionQuiz",
    "Mnożenie małych liczb": "SmallMultiplicationQuiz",
    "Odejmowanie od 10-20": "SubtractionQuiz"
}

# Quiz configuration parameters
DEFAULT_QUIZ_QUESTIONS = 20  # Default number of questions in a quiz 