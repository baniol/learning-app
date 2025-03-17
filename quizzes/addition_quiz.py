"""
Addition quiz implementation with visual aids.
"""
from PySide6.QtCore import Qt
import random
from .base_quiz import BaseQuiz
from .components import NavigationBar, VisualAidWidget

class AdditionQuiz(BaseQuiz):
    """Quiz for practicing addition problems with visual aids."""
    
    def __init__(self):
        """Initialize the addition quiz with visual aids."""
        super().__init__()
        
        # Add navigation bar with visual aid toggle
        self.nav_bar = NavigationBar(self.return_to_menu)
        self.show_visual_aid_checkbox = self.nav_bar.add_checkbox(
            "Show dots helper", True, self.toggle_visual_aid
        )
        self.layout.insertWidget(0, self.nav_bar)
        
        # Add visual aid widget after nav bar
        self.visual_aid = VisualAidWidget(0, 0)
        self.layout.insertWidget(1, self.visual_aid)
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.parent().parent().show_menu()
    
    def toggle_visual_aid(self, state):
        """Toggle the visibility of the visual aid."""
        self.visual_aid.setVisible(self.show_visual_aid_checkbox.isChecked())
        if self.show_visual_aid_checkbox.isChecked():
            self.visual_aid.updateGeometry()
            self.visual_aid.update()
            self.layout.update()
    
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
        was_visible = self.visual_aid.isVisible()
        
        # Update visual aid
        self.visual_aid.deleteLater()
        self.visual_aid = VisualAidWidget(self.num1, self.num2)
        self.layout.insertWidget(1, self.visual_aid)
        
        # Restore visibility state
        self.visual_aid.setVisible(was_visible)
    
    def calculate_answer(self):
        """Calculate the sum of the two numbers."""
        return self.num1 + self.num2
    
    def format_question(self):
        """Format the addition question."""
        return f"{self.num1} + {self.num2} = ?"
    
    def format_question_with_answer(self):
        """Format the addition question with the answer."""
        return f"{self.num1} + {self.num2} = {self.correct_answer}" 