from quiz import Quiz


def create_default_quizzes():
    return [
        Quiz(
            question="지난 잘못을 고쳐 바른길로 돌아간다",
            choices=["이심전심", "개과천선", "유비무환", "동문서답"],
            answers=2
        ),
        Quiz(
            question="미리 준비해 두면 걱정할 일이 없다",
            choices=["유비무환", "일석이조", "자업자득", "금상첨화"],
            answers=1
        ),
        Quiz(
            question="묻는 말과 전혀 상관없는 대답을 한다",
            choices=["동고동락", "역지사지", "이심전심", "동문서답"],
            answers=4
        ),
        Quiz(
            question="상대방의 처지에서 생각해 본다",
            choices=["개과천선", "동문서답", "역지사지", "유비무환"],
            answers=3
        ),
        Quiz(
            question="한 가지 일을 해서 두 가지 이익을 얻는다",
            choices=["금상첨화", "일석이조", "자업자득", "동고동락"],
            answers=2
        )
    ]