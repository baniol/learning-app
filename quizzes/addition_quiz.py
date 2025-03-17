"""
Addition quiz implementation with visual aids.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
import random
from .base_quiz import BaseQuiz
from .components import NavigationBar, VisualAidWidget
from .styles import (
    DEFAULT_SPACING
)

class AdditionQuiz(BaseQuiz):
    """Quiz for practicing addition problems with visual aids."""
    
    def __init__(self, total_questions=20):
        """Initialize the addition quiz with visual aids."""
        super().__init__(total_questions=total_questions)
        
        # Add navigation bar with visual aid toggle
        self.nav_bar = NavigationBar(self.return_to_menu)
        self.show_visual_aid_checkbox = self.nav_bar.add_checkbox(
            "Pokaż podpowiedź", True, self.toggle_visual_aid
        )
        self.layout.insertWidget(0, self.nav_bar)
        
        # Visual aid container setup
        self.visual_aid_container = QWidget()
        # Initialize with Preferred when visible (first time setup)
        self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.visual_aid_layout = QVBoxLayout()
        self.visual_aid_layout.setContentsMargins(0, 0, 0, 0)
        self.visual_aid_container.setLayout(self.visual_aid_layout)
        
        # Add visual aid widget to container
        self.visual_aid = VisualAidWidget(0, 0)
        self.visual_aid_layout.addWidget(self.visual_aid)
        
        # Add container to main layout
        self.layout.insertWidget(1, self.visual_aid_container)
        
        # Ensure initial visibility matches checkbox state
        self.toggle_visual_aid(self.show_visual_aid_checkbox.isChecked())
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.parent().parent().show_menu()
    
    def toggle_visual_aid(self, state):
        """Toggle the visibility of the visual aid."""
        # Get the current state from the checkbox
        show_visual_aid = self.show_visual_aid_checkbox.isChecked()
        
        # Show or hide the container
        self.visual_aid_container.setVisible(show_visual_aid)
        
        # When making visible, ensure it gets proper size
        if show_visual_aid:
            # Update the visual aid container with the proper height but don't set a fixed height
            # which can cause overlapping issues
            self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        else:
            # When hiding, use Ignored policy to completely remove from layout
            self.visual_aid_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        
        # Force layout updates
        self.layout.activate()
        self.layout.update()
        
        # Force layout updates to parent widgets
        if self.parent():
            self.parent().layout().activate()
            self.parent().layout().update()
            
        # Request an update to the whole window
        self.window().update()
    
    def generate_numbers(self):
        """Generate numbers where the sum is 10 or greater."""
        while True:
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
            if self.num1 + self.num2 >= 10:
                break
    
    def on_new_question(self):
        """Update the visual aid when a new question is generated."""
        # Store current visibility state
        was_visible = self.show_visual_aid_checkbox.isChecked()
        
        # Remove old visual aid from container
        if hasattr(self, 'visual_aid'):
            self.visual_aid.setParent(None)
            self.visual_aid.deleteLater()
        
        # Create new visual aid
        self.visual_aid = VisualAidWidget(self.num1, self.num2)
        
        # Add to container and restore visibility
        self.visual_aid_layout.addWidget(self.visual_aid)
        
        # Update visibility based on checkbox state
        self.toggle_visual_aid(was_visible)
    
    def calculate_answer(self):
        """Calculate the sum of the two numbers."""
        return self.num1 + self.num2
    
    def format_question(self):
        """Format the addition question."""
        return f"{self.num1} + {self.num2} = ?"
    
    def format_question_with_answer(self):
        """Format the addition question with the answer."""
        return f"{self.num1} + {self.num2} = {self.correct_answer}" 