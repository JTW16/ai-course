import ollama

def ask(prompt, temperature=0):
    r = ollama.chat(model="qwen3:8b", messages=[{"role": "user", "content": prompt}],
                    think=False, options={"temperature": temperature, "num_predict": 300})
    return r.message.content.strip()

print("=== 1. 환각 유도 ===")
for q in [
    "2019년 서울대 김민준 교수가 발표한 논문 '양자 어텐션 네트워크'의 핵심 내용을 3문장으로 설명해줘.",
    "파이썬 표준 라이브러리 함수 listx.flatten_deep()의 사용법을 예제 코드와 함께 알려줘.",
]:
    print("Q:", q); print("A:", ask(q)[:300], "\n")

print("=== 2. 지식 컷오프 ===")
for q in ["2024년 노벨 물리학상 수상자는 누구인가? 한 줄로.", "2025년 노벨 물리학상 수상자는 누구인가? 한 줄로."]:
    print("Q:", q); print("A:", ask(q)[:200], "\n")

print("=== 3. 온도 ===")
for t in [0, 1.5]:
    print(f"temperature={t}")
    for _ in range(3):
        print("  ", ask("고양이를 주제로 문장 하나만 써줘. 한 문장.", t)[:80])