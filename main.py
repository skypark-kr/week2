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
        
def main():
    while True:
        show_menu()
        choice = read_number("메뉴를 선택하세요: ", 1, 5)
        
        if choice == 1:
            print("퀴즈 풀기")
        elif choice == 2:
            print("퀴즈 추가")
        elif choice == 3:
            print("퀴즈 목록")
        elif choice == 4:
            print("점수 확인")
        elif choice == 5:
            print("퀴즈를 종료합니다.")
            break        
                
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램이 종료되었습니다.")
        
        