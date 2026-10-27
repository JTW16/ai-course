import sys
import ollama
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

data = np.load("index.npz", allow_pickle=True)
chunks, V = data["chunks"], data["vectors"]
V = V / np.linalg.norm(V, axis=1, keepdims=True)      # 미리 정규화해 두면 내적이 코사인이다


def search(question, k=3):
    q = np.array(ollama.embed(model="bge-m3", input=question).embeddings[0])
    q = q / np.linalg.norm(q)
    sims = V @ q
    top = np.argsort(-sims)[:k]
    return [(float(sims[i]), chunks[i]) for i in top]


def answer(question):
    found = search(question)
    context = "\n\n".join(c for _, c in found)
    prompt = f"""아래 자료만 근거로 질문에 답한다. 자료에서 추론할 수 있는 것은 답하고, 자료에 없는 내용은 "자료에 없습니다"라고 답한다. 답은 두 문장 이내로 쓴다.

자료:
{context}

질문: {question}"""
    r = client.chat.completions.create(model="gemma4", temperature=0,
                                       messages=[{"role": "user", "content": prompt}])
    return found, r.choices[0].message.content.strip()


questions = sys.argv[1:] or [
    "수강 철회는 언제까지 할 수 있어?",
    "결석 몇 번까지 괜찮아?",
    "학생증 잃어버리면 얼마 들어?",
    "휴학하고 나서 등록금 돌려받을 수 있어?",
    "기숙사비는 얼마야?",
]
for q in questions:
    found, a = answer(q)
    print("Q:", q)
    for s, c in found:
        print(f"   {s:.3f} {c[:50]}")
    print("   답:", a)
    print()