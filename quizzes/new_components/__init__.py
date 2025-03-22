"""
DEPRECATED: This package is deprecated, use quizzes.components instead.

This package is kept for backward compatibility during the transition.
All imports should be updated to use the components package directly.
"""
import warnings

warnings.warn(
    "The 'new_components' package is deprecated. "
    "Use 'quizzes.components' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from components for backwards compatibility
from ..components.base_component import BaseComponent

__all__ = [
    'BaseComponent'
] 