import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

pairs = [
    ("오늘 날씨가 정말 좋다", "오늘 하늘이 맑고 화창하다"),
    ("오늘 날씨가 정말 좋다", "오늘 날씨가 정말 나쁘다"),
    ("나는 사과를 먹었다", "사과를 나는 먹었다"),
    ("나는 사과를 먹었다", "나는 사과를 먹지 않았다"),
    ("은행에 돈을 맡겼다", "강가의 은행나무 아래 앉았다"),
    ("프로그램이 죽었다", "프로세스가 종료되었다"),
    ("고양이가 소파 위에서 잔다", "개가 마당에서 뛴다"),
    ("회의는 3시에 시작한다", "미팅은 오후 세 시부터다"),
    ("파이썬으로 웹 서버 만드는 법", "자바로 웹 서버 만드는 법"),
    ("사과 가격이 올랐다", "애플 주가가 상승했다"),
    ("나는 사과를 먹었다", "회의는 3시에 시작한다"),
]

for a, b in pairs:
    print(f"{cos(emb(a), emb(b)):.3f}  |  {a}  |  {b}")