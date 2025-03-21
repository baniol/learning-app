"""
Navigation bar component for quiz application.
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox, QLabel, QSpinBox
from ..styles import NAV_BAR_BORDER_STYLE, SUBMENU_BACK_BUTTON_STYLE

class NavigationBar(QWidget):
    """Navigation bar with return button and optional controls."""
    def __init__(self, return_callback, parent=None):
        super().__init__(parent)
        self.setStyleSheet(NAV_BAR_BORDER_STYLE)
        self.setFixedHeight(40)  # Fixed height for nav bar
        
        # Create layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)  # No vertical margins
        self.setLayout(self.layout)
        
        # Add return button
        self.return_button = QPushButton("← Back")
        self.return_button.setMinimumSize(150, 30)
        self.return_button.setStyleSheet(SUBMENU_BACK_BUTTON_STYLE)
        self.return_button.clicked.connect(return_callback)
        self.layout.addWidget(self.return_button)
        
        # Add spacer to push other controls to the right
        self.layout.addStretch()
    
    def add_checkbox(self, label, checked=True, callback=None):
        """Add a checkbox to the navigation bar."""
        checkbox = QCheckBox(label)
        checkbox.setChecked(checked)
        if callback:
            checkbox.stateChanged.connect(callback)
        self.layout.addWidget(checkbox)
        return checkbox
        
    def add_input_mode_toggle(self, checked=False, callback=None):
        """Add a toggle for switching between button and input mode."""
        return self.add_checkbox("Input Mode", checked, callback)
    
    def add_questions_spinbox(self, initial_value=20, min_value=5, max_value=50, callback=None):
        """Add a spin box to select the number of questions."""
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
        
        self.layout.addWidget(container)
        return spinbox 