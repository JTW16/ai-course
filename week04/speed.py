import ollama, subprocess

prompt = "파이썬으로 1부터 100까지 소수를 출력하는 코드를 작성하고, 각 줄에 주석을 달아줘."
for model in ["qwen3:1.7b", "qwen3:8b"]:
    ollama.chat(model=model, think=False, messages=[{"role": "user", "content": "안녕"}])   # 모델을 미리 올린다
    r = ollama.chat(model=model, think=False, messages=[{"role": "user", "content": prompt}],
                    options={"temperature": 0, "num_predict": 300})
    speed = r.eval_count / (r.eval_duration / 1e9)
    ps = subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout.splitlines()
    line = next(l for l in ps if l.startswith(model))
    print(f"{model:11s} {r.eval_count}토큰, 초당 {speed:.1f}토큰 | {line}")