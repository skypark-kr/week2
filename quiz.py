class Quiz:
    def __init__(self, question, choices, answers):
        self.question = question
        self.choices = choices
        self.answers = answers
        self.score = 0
        self.current_question_index = 0
        
    def show(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, selected):
        return selected == self.answers
    