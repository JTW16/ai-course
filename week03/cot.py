import ollama, re

def ask(model, prompt):
    r = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}],
                    think=False, options={"temperature": 0, "num_predict": 400})
    return r.message.content

def last_number(text):
    nums = re.findall(r"-?\d[\d,]*", text.replace(" ", ""))
    return int(nums[-1].replace(",", "")) if nums else None

problems = [
    ("연필 한 자루가 700원이다. 12자루를 사고 10000원을 내면 거스름돈은 얼마인가?", 1600),
    ("교실에 책상이 6줄, 한 줄에 5개 있다. 학생이 27명이면 빈 책상은 몇 개인가?", 3),
    ("기차가 시속 80km로 2시간 30분 달렸다. 이동 거리는 몇 km인가?", 200),
    ("사과 3개 묶음이 4500원이다. 사과 7개를 사려면 얼마인가?", 10500),
    ("어떤 수에 3을 곱하고 7을 더하면 34이다. 그 수는?", 9),
]
styles = {
    "답만": " 답을 숫자만 써라. 풀이 없이.",
    "단계별": " 단계별로 차례로 풀고, 마지막 줄에 '답: 숫자' 형식으로 써라.",
}
for name, suffix in styles.items():
    correct = sum(last_number(ask("qwen3:8b", q + suffix)) == a for q, a in problems)
    print(f"{name:4s} 정답 {correct}/5")