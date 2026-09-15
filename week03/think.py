import ollama, time

q = "어떤 수에 3을 곱하고 7을 더하면 34이다. 그 수는? 답을 숫자만 써라. 풀이 없이."
for think in [False, True]:
    t = time.time()
    r = ollama.chat(model="qwen3:8b", think=think, messages=[{"role": "user", "content": q}],
                    options={"temperature": 0, "num_predict": 1500})
    thinking = r.message.thinking or ""
    print(f"think={think}: 답 {r.message.content.strip()!r}, 생각 {len(thinking)}자, "
          f"{time.time() - t:.1f}초, 출력 토큰 {r.eval_count}")
    if thinking:
        print("생각 앞부분:", thinking[:200].replace("\n", " "))