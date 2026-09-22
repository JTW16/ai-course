import math
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

questions = [
    "대한민국의 수도는? 한 단어로만 답해.",
    "1 + 1 = ? 숫자만 답해.",
    "점심 메뉴 하나만 추천해줘. 음식 이름 한 단어로만 답해.",
    "영어 이름 하나만 지어줘. 이름만.",
]
for q in questions:
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": q}],
                                       max_tokens=1, temperature=0, logprobs=True, top_logprobs=5)
    tops = r.choices[0].logprobs.content[0].top_logprobs
    print(q.split(".")[0])
    print("  ", ", ".join(f"{t.token!r} {math.exp(t.logprob) * 100:.1f}%" for t in tops))