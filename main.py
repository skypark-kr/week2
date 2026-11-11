from quiz import Quiz
from storage import load_quizzes, save_quizzes


def show_menu():
    print("\n === 사자성어 퀴즈 ===")
    print("1. 퀴즈 시작")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    
def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()
        
        if not text:
            print("입력값이 없습니다. 다시 입력해주세요.")
            continue
        
        try:
            number = int(text)
        except ValueError:
            print("숫자가 아닙니다. 다시 입력해주세요.")
            continue
        
        if minimum <= number <= maximum:
            return number
        
        print(f"{minimum}에서 {maximum} 사이의 숫자를 입력해주세요. 다시 입력해주세요.")


class QuizGame:
    def __init__(self):
        self.quizzes = load_quizzes()
        
    def play_quiz(self):
        quizzes = self.quizzes
        if not quizzes:
            print("퀴즈가 없습니다.")
            return
        
        correct_count = 0
        print("\n퀴즈를 시작합니다.")    
        
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n문제 {number}:")
            quiz.show()
            selected = read_number("정답을 선택하세요: ", 1, len(quiz.choices))
            
            if quiz.is_correct(selected):
                print("정답입니다!")
                correct_count += 1
            else:
                correct_choice = quiz.choices[quiz.answers - 1]
                print(f"틀렸습니다. 정답은 {quiz.answers}번입니다.")
                
        print(f"\n퀴즈가 끝났습니다. 총 {len(quizzes)}문제 중 {correct_count}문제를 맞추셨습니다.")
        
    def add_quiz(self):
        print("\n퀴즈 추가")
        
        while True:
            question = input("문제를 입력하세요: ").strip()
            if question:
                break
            print("문제를 입력하지 않았습니다. 다시 입력해주세요.")

        choices = []      
        
        while len(choices) < 4:
            number = len(choices) + 1
            choice = input(f"{number}번 선택지를 입력하세요: ").strip()
            if not choice:
                print("선택지를 입력하지 않았습니다. 다시 입력해주세요.")
                continue
            choices.append(choice)
            
        answers = read_number("정답 번호를 입력하세요: ", 1, len(choices))
        quiz = Quiz(question=question, choices=choices, answers=answers)
        
        update_quizzes = self.quizzes + [quiz]
        save_quizzes(update_quizzes)
        self.quizzes = update_quizzes
        print("퀴즈가 추가되었습니다.")
        
        
    def run(self):
        while True:
            show_menu()
            choice = read_number("메뉴를 선택하세요: ", 1, 5)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                print("퀴즈 목록")
            elif choice == 4:
                print("점수 확인")
            elif choice == 5:
                print("퀴즈를 종료합니다.")
                break        
def main():
    game = QuizGame()
    game.run()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n퀴즈를 종료합니다.")
        
        