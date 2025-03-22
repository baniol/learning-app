"""
Navigation bar component for quiz application.
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox, QLabel, QSpinBox, QComboBox
from PySide6.QtCore import Signal
from ..styles import NAV_BAR_BORDER_STYLE, SUBMENU_BACK_BUTTON_STYLE
from .base_component import BaseComponent

class NavigationBar(BaseComponent):
    """Navigation bar with return button and optional controls."""
    
    # Signal emitted when the current user changes
    user_changed = Signal(int)  # user_id
    
    def __init__(self, return_callback, parent=None):
        """Initialize the navigation bar.
        
        Args:
            return_callback: Function to call when the return button is clicked
            parent: Parent widget
        """
        super().__init__(
            parent=parent,
            style=NAV_BAR_BORDER_STYLE,
            min_height=40  # Fixed height for nav bar
        )
        
        # Create layout
        self.main_layout = self.create_layout(
            orientation='horizontal',
            margins=(5, 0, 5, 0),  # No vertical margins
            spacing=5
        )
        
        # Add return button
        self.return_button = QPushButton("← Back")
        self.return_button.setMinimumSize(150, 30)
        self.return_button.setStyleSheet(SUBMENU_BACK_BUTTON_STYLE)
        self.return_button.clicked.connect(return_callback)
        self.main_layout.addWidget(self.return_button)
        
        # Add spacer to push other controls to the right
        self.add_spacer(self.main_layout)
    
    def add_checkbox(self, label, checked=True, callback=None):
        """Add a checkbox to the navigation bar.
        
        Args:
            label: Label text for the checkbox
            checked: Initial checked state
            callback: Function to call when the checkbox state changes
            
        Returns:
            The created QCheckBox
        """
        checkbox = QCheckBox(label)
        checkbox.setChecked(checked)
        if callback:
            checkbox.stateChanged.connect(callback)
        self.main_layout.addWidget(checkbox)
        return checkbox
        
    def add_input_mode_toggle(self, checked=False, callback=None):
        """Add a toggle for switching between button and input mode.
        
        Args:
            checked: Initial checked state
            callback: Function to call when the toggle state changes
            
        Returns:
            The created QCheckBox
        """
        return self.add_checkbox("Input Mode", checked, callback)
    
    def add_questions_spinbox(self, initial_value=20, min_value=5, max_value=50, callback=None):
        """Add a spin box to select the number of questions.
        
        Args:
            initial_value: Initial value for the spinbox
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            callback: Function to call when the value changes
            
        Returns:
            The created QSpinBox
        """
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        container.setLayout(container_layout)
        
        # Add label
        label = QLabel("Pytania:")
        container_layout.addWidget(label)
        
        # Add spin box
        spinbox = QSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(initial_value)
        spinbox.setFixedWidth(60)
        if callback:
            spinbox.valueChanged.connect(callback)
        container_layout.addWidget(spinbox)
        
        self.main_layout.addWidget(container)
        return spinbox
    
    def add_user_dropdown(self, users, current_user_id=1):
        """
        Add a user selection dropdown to the navigation bar.
        
        Args:
            users: List of user dictionaries with 'id' and 'display_name' keys
            current_user_id: ID of the currently selected user
            
        Returns:
            The created QComboBox
        """
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        container.setLayout(container_layout)
        
        # Add label
        label = QLabel("User:")
        container_layout.addWidget(label)
        
        # Add combobox
        user_combo = QComboBox()
        user_combo.setFixedWidth(150)
        
        # Populate with users
        current_index = 0
        for i, user in enumerate(users):
            user_combo.addItem(user['display_name'], user['id'])
            if user['id'] == current_user_id:
                current_index = i
        
        # Add a special item for adding a new user
        user_combo.addItem("+ Add New User", -1)
        
        # Set current user
        user_combo.setCurrentIndex(current_index)
        
        # Connect signal
        user_combo.currentIndexChanged.connect(self._on_user_changed)
        
        container_layout.addWidget(user_combo)
        self.main_layout.addWidget(container)
        
        self.user_combo = user_combo
        return user_combo
    
    def _on_user_changed(self, index):
        """Handle user selection changes."""
        user_id = self.user_combo.currentData()
        print(f"NavigationBar: User changed to ID: {user_id}, index: {index}")
        
        # Special case for "Add New User"
        if user_id == -1:
            # This will trigger MainWindow.on_user_changed which will show the dialog
            # Just emit the signal with the special ID
            self.user_changed.emit(user_id)
            return
            
        self.user_changed.emit(user_id) 