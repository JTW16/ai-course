import ollama

def ask(system, question):
    r = ollama.chat(model="qwen3:8b", think=False, options={"temperature": 0},
                    messages=[{"role": "system", "content": system},
                              {"role": "user", "content": question}])
    return r.message.content.strip()

q = "파이썬에서 리스트와 튜플의 차이를 설명해줘."
for system in [
    "당신은 친절한 프로그래밍 강사다. 초보자에게 설명한다.",
    "당신은 간결한 기술 문서 작성자다. 세 문장 이내로 답한다. 예제 코드는 넣지 않는다.",
    "당신은 시니어 개발자다. 면접에서 후배를 평가하듯 핵심만 묻고 답한다. 영어로 답한다.",
]:
    print("[시스템]", system)
    print(ask(system, q)[:250], "\n")