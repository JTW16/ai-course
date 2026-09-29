import ollama

MODEL = "qwen3:8b"
history = [{"role": "system", "content": "당신은 프로그래밍 조교다. 한국어로 짧게 답한다. 답 끝에 항상 질문을 하나 던진다."}]

while True:
    try:
        text = input("\n나: ").strip()
    except EOFError:
        break
    if text in ("/bye", "exit"):
        break
    if text == "/reset":
        del history[1:]
        print("(대화 이력을 지웠습니다)")
        continue
    if text == "/history":
        for m in history:
            print(f"  [{m['role']}] {m['content'][:60]}")
        continue
    if not text:
        continue
    history.append({"role": "user", "content": text})
    print("AI: ", end="", flush=True)
    answer = ""
    for chunk in ollama.chat(model=MODEL, messages=history, think=False, stream=True):
        print(chunk.message.content, end="", flush=True)
        answer += chunk.message.content
    print()
    history.append({"role": "assistant", "content": answer})