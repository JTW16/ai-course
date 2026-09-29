from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
stream = client.chat.completions.create(
    model="gemma4", stream=True, stream_options={"include_usage": True},
    messages=[{"role": "user", "content": "봄에 대한 짧은 시를 4줄로 써줘."}],
)
n = 0
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
        n += 1
    if chunk.usage:
        print(f"\n\n조각 {n}개, 입력 {chunk.usage.prompt_tokens} 토큰, 출력 {chunk.usage.completion_tokens} 토큰")