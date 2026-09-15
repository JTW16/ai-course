from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask_server(prompt, temperature=0, max_tokens=300):
    r = client.chat.completions.create(model="gemma4", temperature=temperature, max_tokens=max_tokens,
                                       messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content.strip()

tests = [("농구", "Basketball"), ("야구", "Baseball"), ("축구", "Soccer"), ("펜싱", "Fencing"), ("하키", "Hockey")]
shots = {
    0: "",
    1: "양궁 → Archery\n",
    3: "양궁 → Archery\n골프 → Golf\n컬링 → Curling\n",
}

for k, examples in shots.items():
    correct = 0
    first_answer = None
    for country, capital in tests:
        answer = ask_server(examples + f"{country} →").split("\n")[0]
        if first_answer is None:
            first_answer = answer
        correct += capital in answer
    tail = f"   첫 답: {first_answer}" if correct == 0 else ""
    print(f"gemma4       예시 {k}개  정답 {correct}/5{tail}")