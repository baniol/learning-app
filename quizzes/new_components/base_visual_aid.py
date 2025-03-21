"""
Base class for visual aid components.

This module provides a base class for creating visual aids with standard
functionality for all quiz visual representations.
"""
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt
from .base_component import BaseComponent
from ..styles import VISUAL_AID_BORDER_STYLE, VISUAL_AID_HEIGHT, DEFAULT_SPACING

class BaseVisualAid(BaseComponent):
    """Base class for visual aid components that provide visual representations for quiz problems."""
    
    def __init__(self, num1, num2, parent=None):
        """Initialize the base visual aid.
        
        Args:
            num1: First number to represent
            num2: Second number to represent
            parent: Parent widget
        """
        super().__init__(
            parent=parent,
            style=VISUAL_AID_BORDER_STYLE,
            min_height=VISUAL_AID_HEIGHT
        )
        
        # Set size policy for better layout behavior
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Store the numbers
        self.num1 = num1
        self.num2 = num2
        
        # Main layout
        self.main_layout = self.create_layout(
            orientation='horizontal',
            spacing=DEFAULT_SPACING
        )
        
        # Initialize the visual components
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize the visual components.
        
        This method should be overridden by subclasses to set up their specific
        visual representations of the numbers.
        """
        pass
    
    def update_numbers(self, num1, num2):
        """Update the numbers and refresh the visual representation.
        
        Args:
            num1: New first number
            num2: New second number
        """
        self.num1 = num1
        self.num2 = num2
        self.refresh_visual()
    
    def refresh_visual(self):
        """Refresh the visual representation based on the current numbers.
        
        This method should be overridden by subclasses to update their specific
        visual representations when the numbers change.
        """
        pass 