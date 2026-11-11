import json
from pathlib import Path

from quiz import Quiz
from quiz_data import create_default_quizzes

state_file = Path(__file__).with_name("state.json")

def save_quizzes(quizzes):
    data = {
        "quizzes": [
            {
                "question": quiz.question,
                "choices": quiz.choices,
                "answers": quiz.answers
            }
            for quiz in quizzes
        ]
    }
    
    data["scores"] = load_scores()
    
    with state_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    
def load_quizzes():
    try:
        with state_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
            
            rows = data["quizzes"]
            if not isinstance(rows, list):
                raise ValueError("퀴즈 목록 오류")
            
            quizzes = []
            for row in rows:
                question = row["question"]
                choices = row["choices"]
                answers = row["answers"]
                
                if not isinstance(question, str) or not question.strip():
                    raise ValueError("퀴즈 질문 오류")
                if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
                    raise ValueError("퀴즈 선택지 오류")
                if type(answers) is not int or not 1 <= answers <= len(choices):
                    raise ValueError("퀴즈 정답 오류")
                
                quizzes.append(Quiz(question=question, choices=choices, answers=answers))
                
            return quizzes
    
    except FileNotFoundError:
        print("퀴즈 상태 파일이 존재하지 않습니다. 기본 퀴즈를 생성합니다.")
    except (ValueError, KeyError, TypeError):
        print(f"퀴즈 상태 파일 오류: {e}. 기본 퀴즈를 생성합니다.")
    
    quizzes = create_default_quizzes()
    save_quizzes(quizzes)
    return quizzes

def load_scores():
    try:
        with state_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, ValueError):
        return []
    
    if isinstance(data, dict) and isinstance(data.get("scores"), list):
        return data["scores"]
    
def save_scores(correct, total):
    with state_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
        
        scores = data.setdefault("scores", [])
        scores.append({"correct": correct, "total": total})
        
    with state_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        