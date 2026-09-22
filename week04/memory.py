import ollama

def chat(messages):
    r = ollama.chat(model="qwen3:8b", think=False, messages=messages, options={"temperature": 0})
    return r.message.content.strip()

first = chat([{"role": "user", "content": "내 이름은 최민수야. 기억해 줘. 한 줄로 답해."}])
print("1:", first)

print("2 (이전 대화 없이):", chat([{"role": "user", "content": "내 이름이 뭐라고 했지? 한 줄로."}]))

print("3 (이전 대화 포함):", chat([
    {"role": "user", "content": "내 이름은 최민수야. 기억해 줘. 한 줄로 답해."},
    {"role": "assistant", "content": first},
    {"role": "user", "content": "내 이름이 뭐라고 했지? 한 줄로."},
]))