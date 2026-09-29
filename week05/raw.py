import json, urllib.request

body = {
    "model": "qwen3:8b",
    "messages": [{"role": "user", "content": "파이썬에서 리스트를 뒤집는 방법을 한 줄로."}],
    "stream": False,
    "think": False,
}
req = urllib.request.Request("http://localhost:11434/api/chat",
                             data=json.dumps(body).encode("utf-8"),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

print(json.dumps(data, ensure_ascii=False, indent=2))
print("\n답만:", data["message"]["content"])
print("생성 속도:", round(data["eval_count"] / (data["eval_duration"] / 1e9), 1), "tok/s")