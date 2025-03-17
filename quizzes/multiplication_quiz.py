from .base_quiz import BaseQuiz

class MultiplicationQuiz(BaseQuiz):
    def calculate_answer(self):
        return self.num1 * self.num2

    def format_question(self):
        return f"{self.num1} × {self.num2} = ?"

    def format_question_with_answer(self):
        return f"{self.num1} × {self.num2} = {self.correct_answer}" 