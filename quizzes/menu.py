"""
Menu components for the quiz application.
"""
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QFont
import quizzes.styles as styles
from quizzes.mappings import MENU_CATEGORIES, SUBMENU_ITEMS, QUIZ_TYPE_MAP

# Define icons for each category
CATEGORY_ICONS = {
    "Math": "icons/math.png",
    "Languages": "icons/languages.png",
    "Settings": "icons/settings.png",
    "Stats": "icons/stats.png"
}

class SubMenu(QWidget):
    """Submenu with buttons for a specific category."""
    
    # Signal to notify when a quiz is selected
    quiz_selected = Signal(str)
    # Signal to go back to main menu
    back_to_main = Signal()
    
    def __init__(self, category, items, parent=None):
        super().__init__(parent)
        self.category = category
        self.items = items
        self.setStyleSheet(styles.MENU_CONTAINER_BORDER_STYLE)
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)
        
        # Header with category title and back button
        self.header_layout = QHBoxLayout()
        
        self.back_button = QPushButton("← Back")
        self.back_button.setStyleSheet(styles.SUBMENU_BACK_BUTTON_STYLE)
        self.back_button.setFixedWidth(100)
        self.back_button.clicked.connect(self.on_back_button_click)
        self.header_layout.addWidget(self.back_button)
        
        self.category_label = QLabel(category)
        self.category_label.setStyleSheet(styles.SUBMENU_HEADER_STYLE)
        self.category_label.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.category_label, 1)  # Stretch factor 1
        
        # Add empty widget for symmetry
        self.spacer = QWidget()
        self.spacer.setFixedWidth(100)
        self.header_layout.addWidget(self.spacer)
        
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addSpacing(10)
        
        # Buttons grid
        self.buttons_layout = QGridLayout()
        self.buttons_layout.setSpacing(styles.MENU_LAYOUT_SPACING)
        
        # Add buttons in a grid (3 columns)
        for i, item in enumerate(items):
            button = QPushButton(item)
            button.setMinimumSize(*styles.MENU_BUTTON_SIZE)
            button.setStyleSheet(styles.MENU_BUTTON_STYLE)
            button.clicked.connect(lambda checked, name=item: self.on_button_click(name))
            
            # Style the button differently if it's implemented
            if item in QUIZ_TYPE_MAP:
                button.setStyleSheet(styles.MENU_BUTTON_STYLE)
            else:
                button.setStyleSheet(styles.MENU_BUTTON_DISABLED_STYLE)
                
            self.buttons_layout.addWidget(button, i // 3, i % 3)
        
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addStretch(1)  # Add stretch to push content to top
    
    def on_button_click(self, name):
        """Handle button clicks and emit quiz_selected signal."""
        if name in QUIZ_TYPE_MAP:
            self.quiz_selected.emit(name)
        else:
            print(f"{name} clicked - not implemented yet")
    
    def on_back_button_click(self):
        """Emit signal to go back to main menu."""
        self.back_to_main.emit()

class MainMenu(QWidget):
    """Main menu with category selection buttons and submenus."""
    
    # Signal to notify when a quiz is selected
    quiz_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.MENU_CONTAINER_BORDER_STYLE)
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)
        
        # Title
        self.title_label = QLabel("Quiz Application")
        self.title_label.setStyleSheet(styles.MAIN_MENU_TITLE_STYLE)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Select a category:")
        self.subtitle_label.setStyleSheet(styles.MAIN_MENU_SUBTITLE_STYLE)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.subtitle_label)
        self.main_layout.addSpacing(20)
        
        # Stacked widget to manage main menu and submenus
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Create main menu page
        self.main_menu_widget = QWidget()
        self.main_menu_layout = QGridLayout()
        self.main_menu_layout.setSpacing(styles.MENU_LAYOUT_SPACING)
        self.main_menu_widget.setLayout(self.main_menu_layout)
        
        # Add category buttons to grid (2 rows, 2 columns)
        for i, category in enumerate(MENU_CATEGORIES):
            button = QPushButton(category)
            button.setMinimumSize(*styles.MENU_BUTTON_SIZE)
            button.setStyleSheet(styles.MENU_BUTTON_STYLE)
            
            # Add icon if available
            if category in CATEGORY_ICONS:
                button.setIcon(QIcon(CATEGORY_ICONS[category]))
                button.setIconSize(QSize(*styles.MENU_BUTTON_ICON_SIZE))
            
            button.clicked.connect(lambda checked, cat=category: self.show_submenu(cat))
            self.main_menu_layout.addWidget(button, i // 2, i % 2)
        
        # Add main menu to stacked widget
        self.stacked_widget.addWidget(self.main_menu_widget)
        
        # Create submenus for each category
        self.submenus = {}
        for category, items in SUBMENU_ITEMS.items():
            submenu = SubMenu(category, items)
            submenu.quiz_selected.connect(self.on_quiz_selected)
            submenu.back_to_main.connect(self.show_main_menu)
            self.submenus[category] = submenu
            self.stacked_widget.addWidget(submenu)
    
    def show_submenu(self, category):
        """Switch to the submenu for the selected category."""
        self.stacked_widget.setCurrentWidget(self.submenus[category])
    
    def show_main_menu(self):
        """Switch back to the main menu."""
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
    
    def on_quiz_selected(self, name):
        """Forward the quiz_selected signal from submenu."""
        self.quiz_selected.emit(name) 