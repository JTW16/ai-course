import ollama

secret = "비밀 번호는 4127이다."
filler = "오늘 날씨는 맑고 바람이 조금 분다. 학교 가는 길에 편의점에 들러 우유를 샀다. "

for num_ctx in [2048, 3000, 4000, 5000, 8192]:
    for reps in [20, 60, 120]:
        text = secret + " " + filler * reps + "\n\n위 글에 나온 비밀 번호는? 숫자만."
        r = ollama.chat(model="qwen3:8b", think=False, messages=[{"role": "user", "content": text}],
                        options={"temperature": 0, "num_ctx": num_ctx, "num_predict": 20})
        print(f"num_ctx={num_ctx} 반복 {reps} ({len(text)}자): {r.message.content.strip()[:40]!r}")