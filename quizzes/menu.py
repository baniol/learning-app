"""
Menu components for the quiz application.
"""
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Signal
import quizzes.styles as styles

class MainMenu(QWidget):
    """Main menu with quiz selection buttons."""
    
    # Signal to notify when a quiz is selected
    quiz_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.MENU_CONTAINER_BORDER_STYLE)
        
        # Setup layout
        self.menu_layout = QGridLayout()
        self.menu_layout.setSpacing(styles.MENU_LAYOUT_SPACING)
        self.setLayout(self.menu_layout)
        
        # Add buttons to grid (2 rows, 3 columns)
        for i, item in enumerate(styles.MENU_ITEMS):
            button = QPushButton(item)
            button.setMinimumSize(*styles.MENU_BUTTON_SIZE)
            button.setStyleSheet(styles.MENU_BUTTON_STYLE)
            button.clicked.connect(lambda checked, name=item: self.on_button_click(name))
            self.menu_layout.addWidget(button, i // 3, i % 3)
    
    def on_button_click(self, name):
        """Handle button clicks and emit quiz_selected signal."""
        if name in styles.QUIZ_TYPE_MAP:
            self.quiz_selected.emit(name)
        else:
            print(f"{name} clicked") 