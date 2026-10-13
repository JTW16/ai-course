import random

def parse_guess(text: str):
    stripped = text.strip()
    if not stripped:
        return "숫자를 입력하세요"

    # isdigit()만 쓰면 전각 숫자(５０)나 위첨자(²)도 통과하므로 ASCII로 제한
    if not (stripped.isascii() and stripped.isdigit()):
        return "1부터 100 사이의 정수를 입력하세요"

    val = int(stripped)
    if val < 1 or val > 100:
        return "1부터 100 사이의 정수를 입력하세요"

    return val

def judge(guess: int, answer: int) -> str:
    if guess < answer:
        return "더 큽니다"
    elif guess > answer:
        return "더 작습니다"
    else:
        return "정답"

class Game:
    def __init__(self, answer=None):
        if answer is not None:
            self.answer = answer
        else:
            self.answer = random.randint(1, 100)
        self.result = ""
        self.notice = ""
        self.attempts = 0
        self.history = []
        self.over = False
        self.best = None

    def submit(self, text: str):
        if self.over:
            return

        parsed = parse_guess(text)

        if isinstance(parsed, str):
            self.notice = parsed
            return

        # history는 "30 (더 큽니다)" 형태의 문자열이므로 앞부분으로 중복을 찾는다
        for entry in self.history:
            if entry.startswith(f"{parsed} ("):
                self.notice = "이미 입력한 숫자입니다"
                return

        res = judge(parsed, self.answer)
        self.attempts += 1
        self.notice = ""
        if res == "정답":
            self.result = f"정답! {self.attempts}번 만에 맞혔습니다"
            self.over = True
            if self.best is None or self.best > self.attempts:
                self.best = self.attempts
        else:
            self.result = res
        self.history.append(f"{parsed} ({res})")

    def new_game(self):
        self.answer = random.randint(1, 100)
        self.result = ""
        self.notice = ""
        self.attempts = 0
        self.history = []
        self.over = False
