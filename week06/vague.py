import re
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

prompt = "전화번호를 정리하는 함수 만들어줘."

for i in range(5):
    r = client.chat.completions.create(
        model="gemma4", temperature=0.7, max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = r.choices[0].message.content
    open(f"vague_{i + 1}.txt", "w", encoding="utf-8").write(text)
    print(f"--- {i + 1}회")
    for line in re.findall(r"^def .*", text, re.M):
        print(line)