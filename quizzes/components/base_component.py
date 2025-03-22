"""
Base component class for UI widgets.

This module provides a base class for UI components to standardize initialization
and reduce code duplication across the application.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

class BaseComponent(QWidget):
    """Base class for UI components with common functionality.
    
    This class provides common setup and utility methods for UI components
    to reduce boilerplate code and standardize component creation.
    """
    
    def __init__(self, parent=None, style=None, min_height=None, min_width=None):
        """Initialize the base component with common setup.
        
        Args:
            parent: Parent widget
            style: CSS stylesheet to apply
            min_height: Minimum height for the component
            min_width: Minimum width for the component
        """
        super().__init__(parent)
        
        if style:
            self.setStyleSheet(style)
        
        if min_height:
            self.setMinimumHeight(min_height)
        
        if min_width:
            self.setMinimumWidth(min_width)
    
    def create_layout(self, orientation='vertical', margins=(0, 0, 0, 0), spacing=10):
        """Create a layout for the component.
        
        Args:
            orientation: 'vertical' or 'horizontal'
            margins: Tuple of (left, top, right, bottom) margins
            spacing: Spacing between elements
            
        Returns:
            The created layout
        """
        if orientation == 'vertical':
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()
        
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)
        self.setLayout(layout)
        return layout
    
    def add_spacer(self, layout=None, expandable=True):
        """Add a spacer to the layout.
        
        Args:
            layout: Layout to add spacer to (uses self.layout() if None)
            expandable: Whether the spacer should expand to fill space
        """
        if layout is None:
            layout = self.layout()
        
        if expandable:
            layout.addStretch()
        else:
            layout.addSpacing(10) 