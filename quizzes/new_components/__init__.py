"""
UI components package for the quiz application.

This package contains reusable UI components used across different quizzes.
"""
from .base_component import BaseComponent
from .base_visual_aid import BaseVisualAid

# These components still need to be migrated from the old file
# Don't import them here to avoid circular imports

__all__ = [
    'BaseComponent',
    'BaseVisualAid'
] 