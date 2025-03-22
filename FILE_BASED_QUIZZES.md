# Creating File-Based Quizzes

You can create custom quizzes without writing any code by using JSON files to define your questions and answers.

## JSON File Format

Each quiz file should contain an array of question-answer pairs in JSON format:

```json
[
  {
    "question": "Question text goes here?",
    "answer": "Answer text goes here"
  },
  {
    "question": "Another question?",
    "answer": "Another answer"
  }
]
```

Requirements:
- Each question must have both a `question` and an `answer` field
- The file must be valid JSON
- The file must contain an array of question objects

## Steps to Create a New Quiz

1. Create a JSON file with your questions and answers
2. Save it in the `quizzes/` directory with a descriptive name
3. Register the quiz in `quiz_manager.py`
4. Add the quiz to the menu in `mappings.py`

### Example: Adding a Vocabulary Quiz

1. **Create the JSON file** (`quizzes/spanish_vocab.json`):

```json
[
  {
    "question": "What is 'hello' in Spanish?",
    "answer": "Hola"
  },
  {
    "question": "What is 'thank you' in Spanish?",
    "answer": "Gracias"
  },
  {
    "question": "What is 'goodbye' in Spanish?",
    "answer": "Adiós"
  }
]
```

2. **Register the quiz in `quiz_manager.py`**:

```python
# Inside _load_quizzes method
self.register_quiz("SpanishVocabQuiz", create_quiz_from_file(
    "quizzes/spanish_vocab.json",
    "Spanish Vocabulary"
))
```

3. **Add to menu in `mappings.py`**:

```python
# Add to SUBMENU_ITEMS
"Languages": [
    "English Words",
    "Spanish Words",
    "Spanish Vocabulary"  # New item
],

# Add to QUIZ_TYPE_MAP
"Spanish Vocabulary": "SpanishVocabQuiz",
```

## Advanced Options

When creating a quiz, you can specify additional options:

```python
create_quiz_from_file(
    file_path="quizzes/my_quiz.json",
    quiz_name="My Custom Quiz",
    input_mode="self_assess",  # "self_assess", True for input field, False for buttons
    shuffle=True,              # Whether to shuffle questions
    total_questions=10         # Limit number of questions (or None for all)
)
```

## Integrating with Custom Code

You can also extend the `FileBasedQuiz` class for more customization:

```python
from quizzes.file_based_quiz import FileBasedQuiz

class MyCustomQuiz(FileBasedQuiz):
    def __init__(self, parent=None):
        super().__init__(
            file_path="quizzes/my_questions.json",
            parent=parent,
            input_mode="self_assess"
        )
        # Additional customization here
        
    def format_question(self):
        # Custom question formatting
        return f"Q: {self.current_question_text}"
``` 