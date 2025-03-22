"""
Quiz manager for centralized quiz creation and management.

This module provides a central manager for creating, registering, and retrieving
quiz classes in the application.
"""
from .mappings import QUIZ_TYPE_MAP

class QuizManager:
    """Manager for quiz classes that provides centralized access to quiz types."""
    
    def __init__(self):
        """Initialize the quiz manager."""
        self._quiz_registry = {}
        self._loaded = False
    
    def register_quiz(self, name, quiz_class):
        """Register a quiz class with a given name.
        
        Args:
            name: The name of the quiz (should match entry in QUIZ_TYPE_MAP)
            quiz_class: The class to register
            
        Returns:
            The registered quiz class (for chaining)
        """
        self._quiz_registry[name] = quiz_class
        return quiz_class
    
    def get_quiz_class(self, name):
        """Get a quiz class by name.
        
        Args:
            name: The name of the quiz
            
        Returns:
            The quiz class or None if not found
        """
        if not self._loaded:
            self._load_quizzes()
        
        return self._quiz_registry.get(name)
    
    def create_quiz(self, name, **kwargs):
        """Create a quiz instance by name.
        
        Args:
            name: The name of the quiz
            **kwargs: Arguments to pass to the quiz constructor
            
        Returns:
            A new quiz instance or None if the quiz class is not found
        """
        quiz_class = self.get_quiz_class(name)
        if quiz_class:
            return quiz_class(**kwargs)
        return None
    
    def create_simple_quiz(self, name, quiz_class, **kwargs):
        """Create and register a quiz in one simple step.
        
        Args:
            name: The name to register the quiz with
            quiz_class: The quiz class to register
            **kwargs: Default arguments for the quiz when created
            
        Returns:
            The registered quiz class
        """
        self.register_quiz(name, quiz_class)
        return quiz_class
    
    def get_all_quiz_names(self):
        """Get a list of all registered quiz names.
        
        Returns:
            List of quiz names
        """
        if not self._loaded:
            self._load_quizzes()
            
        return list(self._quiz_registry.keys())
    
    def _load_quizzes(self):
        """Load all quiz classes defined in the types package.
        
        This lazy loads the quiz classes when first needed.
        """
        from .types import (
            AdditionQuiz,
            MultiplicationQuiz,
            SmallMultiplicationQuiz,
            SubtractionQuiz
        )
        
        # Register by class name (as defined in QUIZ_TYPE_MAP)
        self.register_quiz("AdditionQuiz", AdditionQuiz)
        self.register_quiz("MultiplicationQuiz", MultiplicationQuiz)
        self.register_quiz("SmallMultiplicationQuiz", SmallMultiplicationQuiz)
        self.register_quiz("SubtractionQuiz", SubtractionQuiz)
        
        self._loaded = True

# Create a singleton instance
quiz_manager = QuizManager() 