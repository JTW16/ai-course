import ollama, json

prompt = """다음 문장에서 이름, 학과, 학년을 뽑아 JSON으로만 답해. 키는 name, dept, year.
문장: 소프트웨어학부 2학년 김민수는 이번 학기에 자료구조를 듣는다."""
r = ollama.chat(model="qwen3:8b", think=False, format="json",
                messages=[{"role": "user", "content": prompt}])
print("원문:", r.message.content)
info = json.loads(r.message.content)
print("파싱:", info["name"], "/", info["dept"], "/", info["year"])