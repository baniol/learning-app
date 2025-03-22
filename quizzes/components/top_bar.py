"""
Top bar component for quiz application.
Contains the app title and user navigation bar.
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from ..debug import log
from .. import styles
from .base_component import BaseComponent

class TopBar(BaseComponent):
    """Top bar component with app title and user navigation."""
    
    def __init__(self, user_manager, parent=None):
        """
        Initialize the top bar.
        
        Args:
            user_manager: The UserManager instance to use for the nav bar
            parent: Parent widget
        """
        super().__init__(
            parent=parent,
            style=styles.NAV_BAR_BORDER_STYLE,
            min_height=50
        )
        self.user_manager = user_manager
        
        log("TopBar", "Initializing")
        
        # Layout
        self.main_layout = self.create_layout(
            orientation='horizontal',
            margins=(10, 5, 10, 5)
        )
        
        self.setup_app_title()
        self.setup_user_nav()
        
        log("TopBar", "Initialization complete")
    
    def setup_app_title(self):
        """Set up the application title on the left side."""
        # App title
        title_label = QLabel("Quiz App")
        title_label.setStyleSheet(styles.APP_TITLE_STYLE)
        self.main_layout.addWidget(title_label)
        
        # Add spacer between title and user nav
        self.add_spacer(self.main_layout)
    
    def setup_user_nav(self):
        """Set up the user navigation section on the right side."""
        # User dropdown
        self.user_selection = self.user_manager.create_user_selector()
        self.main_layout.addWidget(self.user_selection) 