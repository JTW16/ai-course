from openai import OpenAI

servers = {
    "내 PC (Ollama)": OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),
    "실습 서버 (vLLM)": OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none"),
}
models = {"내 PC (Ollama)": "qwen3:8b", "실습 서버 (vLLM)": "gemma4"}
question = "파이썬에서 리스트와 튜플의 차이를 한 문장으로."

for name, client in servers.items():
    r = client.chat.completions.create(model=models[name], max_tokens=200,
                                       messages=[{"role": "user", "content": question}])
    print(f"[{name}] {r.choices[0].message.content.strip()[:120]}")
    print(f"   입력 {r.usage.prompt_tokens} 토큰, 출력 {r.usage.completion_tokens} 토큰")