from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask_server(prompt, temperature=0, max_tokens=300):
    r = client.chat.completions.create(model="gemma4", temperature=temperature, max_tokens=max_tokens,
                                       messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content.strip()

print([m.id for m in client.models.list().data])
print(ask_server("안녕? 너는 어떤 모델이야? 한 문장으로."))