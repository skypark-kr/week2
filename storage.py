import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from quiz import Quiz
from quiz_data import create_default_quizzes


state_file = Path(__file__).with_name("state.json")
backup_file = state_file.with_suffix(".json.bak")


# 1. Quiz 객체 목록을 JSON에 저장할 수 있는 목록으로 바꾼다.
def quiz_rows(quizzes):
    rows = []

    for quiz in quizzes:
        row = {
            "question": quiz.question,
            "choices": quiz.choices,
            "answers": quiz.answers
        }
        rows.append(row)

    return rows


# 2. 지정한 JSON 파일을 읽고 문제와 점수의 형식을 확인한다.
def read_state(path):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
        raise ValueError("퀴즈 목록 오류")

    for row in data["quizzes"]:
        question = row["question"]
        choices = row["choices"]
        answers = row["answers"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("퀴즈 질문 오류")
        if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
            raise ValueError("퀴즈 선택지 오류")
        if type(answers) is not int or not 1 <= answers <= len(choices):
            raise ValueError("퀴즈 정답 오류")

    # 점수 기능을 추가하기 전에 만든 파일에는 scores가 없을 수 있다.
    if data.get("scores") is None:
        data["scores"] = []

    if not isinstance(data["scores"], list):
        raise ValueError("점수 목록 오류")

    for score in data["scores"]:
        correct = score["correct"]
        total = score["total"]

        if type(correct) is not int or type(total) is not int:
            raise ValueError("점수 항목 오류")
        if not 0 <= correct <= total:
            raise ValueError("점수 범위 오류")

    return data


# 3. 임시 파일에 먼저 쓴 뒤 대상 파일을 교체한다.
def write_json(path, data):
    temp_path = None

    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False
        ) as file:
            temp_path = Path(file.name)
            json.dump(data, file, ensure_ascii=False, indent=2)

        temp_path.replace(path)

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


# 4. 직전 상태를 백업하고 새 상태를 원본에 저장한다.
def save_state(data, previous=None):
    if previous is not None:
        write_json(backup_file, previous)

    write_json(state_file, data)


# 5. 원본 → 백업 → 기본 문제 순서로 게임 데이터를 불러온다.
def load_state():
    try:
        return read_state(state_file)
    except (FileNotFoundError, ValueError, KeyError, TypeError):
        pass

    try:
        data = read_state(backup_file)
        print("백업에서 퀴즈와 점수를 복구합니다.")
    except (FileNotFoundError, ValueError, KeyError, TypeError):
        print("사용할 저장 파일이 없어 기본 퀴즈를 생성합니다.")
        data = {
            "quizzes": quiz_rows(create_default_quizzes()),
            "scores": []
        }

    save_state(data)
    return data


# 6. 저장된 문제를 게임에서 사용하는 Quiz 객체로 바꾼다.
def load_quizzes():
    data = load_state()
    quizzes = []

    for row in data["quizzes"]:
        quiz = Quiz(
            question=row["question"],
            choices=row["choices"],
            answers=row["answers"]
        )
        quizzes.append(quiz)

    return quizzes


# 7. 저장된 점수 목록을 가져온다.
def load_scores():
    data = load_state()
    return data["scores"]


# 8. 문제 목록을 갱신하고 기존 점수와 함께 저장한다.
def save_quizzes(quizzes):
    previous = load_state()
    updated = previous.copy()
    updated["quizzes"] = quiz_rows(quizzes)

    save_state(updated, previous)


# 9. 새 점수 한 건을 추가하고 기존 문제와 함께 저장한다.
def save_scores(correct, total):
    previous = load_state()
    updated = previous.copy()
    new_score = {"correct": correct, "total": total}
    updated["scores"] = previous["scores"] + [new_score]

    save_state(updated, previous)