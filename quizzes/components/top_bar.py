"""
Top bar component for quiz application.
Contains the app title and user navigation bar.
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from ..debug import log
from .. import styles

class TopBar(QWidget):
    """Top bar component with app title and user navigation."""
    
    def __init__(self, user_manager, parent=None):
        """
        Initialize the top bar.
        
        Args:
            user_manager: The UserManager instance to use for the nav bar
            parent: Parent widget
        """
        super().__init__(parent)
        self.user_manager = user_manager
        
        log("TopBar", "Initializing")
        
        # Setup UI
        self.setFixedHeight(50)
        self.setStyleSheet(styles.NAV_BAR_BORDER_STYLE)
        
        # Layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.setLayout(self.layout)
        
        self.setup_app_title()
        self.setup_user_nav()
        
        log("TopBar", "Initialization complete")
    
    def setup_app_title(self):
        """Set up the app title section."""
        # Container for app title
        title_container = QWidget()
        title_container.setFixedWidth(200)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_container.setLayout(title_layout)
        
        # App title label
        app_title = QLabel("Quiz App")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(app_title)
        
        self.layout.addWidget(title_container)
        
        # Add spacer to push nav to the right
        self.layout.addStretch(1)
    
    def setup_user_nav(self):
        """Set up the user navigation section."""
        # Setup user navigation bar with no return callback
        nav_bar = self.user_manager.setup_navigation_bar(lambda: None)
        self.layout.addWidget(nav_bar) 