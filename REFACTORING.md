# Refactoring Overview

This document outlines the refactoring changes made to improve the structure, clarity, and extensibility of the quiz application.

## Key Improvements

1. **Base Component System**
   - Created `BaseComponent` class to standardize UI component creation
   - Reduced boilerplate code by centralizing common functionality
   - Improved layout management with helper methods

2. **Visual Aid Architecture**
   - Created `BaseVisualAid` to standardize visual aid implementations
   - Simplified creation of new visual aids with a clear template
   - Standardized number handling and updates

3. **Component Organization**
   - Organized components into a proper package structure 
   - Improved imports and component discovery
   - Reduced code duplication

4. **Quiz Management**
   - Created a `QuizManager` singleton to handle quiz creation centrally
   - Simplified quiz discovery and instantiation
   - Standardized quiz registration process

5. **Better Type Hints & Documentation**
   - Added type hints to improve code clarity and IDE support
   - Enhanced documentation for easier maintenance
   - Broke down complex methods into smaller, focused ones

6. **Cleaner BaseQuiz Structure**
   - Refactored initialization into smaller, specific methods
   - Made the class easier to understand and extend
   - Standardized feedback and state handling

## How to Use the New Structure

### Creating a Component

```python
from quizzes.components.base_component import BaseComponent

class MyComponent(BaseComponent):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            style="your-css-style",
            min_height=100
        )
        
        # Create layout with helper method
        self.main_layout = self.create_layout(
            orientation='vertical',
            margins=(10, 10, 10, 10),
            spacing=5
        )
        
        # Add your components here
        
        # Add a spacer
        self.add_spacer()
```

### Creating a Visual Aid

```python
from quizzes.components.base_visual_aid import BaseVisualAid

class MyVisualAid(BaseVisualAid):
    def __init__(self, num1, num2, parent=None):
        super().__init__(num1, num2, parent)
        
    def initialize_components(self):
        # Set up your visual representation here
        pass
        
    def refresh_visual(self):
        # Update visual when numbers change
        pass
```

### Using the Quiz Manager

```python
from quizzes.quiz_manager import quiz_manager

# Get a quiz class
AdditionQuiz = quiz_manager.get_quiz_class("AdditionQuiz")

# Create a quiz instance
quiz = quiz_manager.create_quiz(
    "AdditionQuiz", 
    total_questions=10, 
    show_questions_control=True
)

# Get all quiz names
all_quizzes = quiz_manager.get_all_quiz_names()
```

### Registering a New Quiz

```python
from quizzes.quiz_manager import quiz_manager

# Define your quiz class
class MyCustomQuiz(BaseQuiz):
    # Implement your quiz here
    pass

# Register it 
quiz_manager.register_quiz("MyCustomQuiz", MyCustomQuiz)

# Add to mappings.py
QUIZ_TYPE_MAP = {
    "My Custom Quiz": "MyCustomQuiz",
    # ... other mappings
}
```

## Next Steps

1. **Migrate Components Properly**
   - Move classes from `components.py` into separate files in the `new_components` directory
   - For each component:
     - Create a new file in `new_components/`
     - Move the class implementation
     - Update imports
   - After all components are migrated, rename `new_components` back to `components`
   - Update all imports across the codebase

2. **Add More Type Hints**
   - Continue adding type hints to more files
   - Use mypy to check type correctness

3. **Improve Testing**
   - Add unit tests for core functionality
   - Set up testing framework

4. **Enhance Error Handling**
   - Add more robust error handling
   - Implement graceful fallback behaviors

5. **Further Documentation**
   - Add docstrings to all public methods
   - Create more examples 

## Dealing with Circular Imports

When restructuring the codebase, we encountered circular imports between the new components package and existing code. Here's how we resolved it:

1. **Identify the circular dependency**:
   - The circular import occurred when `quizzes/components/__init__.py` tried to import from `quizzes.components` while itself being part of that package.

2. **Temporary renaming**:
   - We temporarily renamed the `components` directory to `new_components` to avoid namespace conflicts
   - This allowed imports from the original `components.py` file to work while we gradually migrate

3. **Gradual migration path**:
   - Keep using `components.py` for existing components
   - Create new components in the `new_components` directory
   - Gradually move classes from `components.py` to separate files in `new_components/`
   - Update imports as needed

4. **Final step**:
   - Once all components are migrated, rename `new_components` back to `components`
   - Remove the old `components.py` file 