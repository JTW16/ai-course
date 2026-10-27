import sys
import sqlite3
import ollama
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
con = sqlite3.connect("campus.db")

rows = con.execute("SELECT id, name, area, walk_min, hours, category, description, embedding FROM facility").fetchall()
V = np.stack([np.frombuffer(r[-1], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)


def search(question, k=3):
    q = np.array(ollama.embed(model="bge-m3", input=question).embeddings[0])
    q = q / np.linalg.norm(q)
    sims = V @ q
    return [(float(sims[i]), rows[i][:-1]) for i in np.argsort(-sims)[:k]]


def answer(question):
    found = search(question)
    context = "\n".join(f"- {name} ({area}, 도보 {walk_min}분, {hours}, {cat}): {desc}"
                        for _, (id_, name, area, walk_min, hours, cat, desc) in found)
    prompt = f"""아래 식당 목록만 근거로 질문에 답한다. 목록에 없는 내용은 "자료에 없습니다"라고 답한다. 답은 두 문장 이내로 쓴다.

식당 목록:
{context}

질문: {question}"""
    r = client.chat.completions.create(model="gemma4", temperature=0,
                                       messages=[{"role": "user", "content": prompt}])
    return found, r.choices[0].message.content.strip()


questions = sys.argv[1:] or [
    "새벽에 해장할 데 있어?",
    "집에서 짜장면 시켜 먹고 싶어",
    "고기 실컷 먹고 싶은데 차 가져가도 돼?",
    "혼밥하기 좋은 데 어디야?",
    "호계동에 오마카세 집 있어?",
]
for q in questions:
    found, a = answer(q)
    print("Q:", q)
    for s, (id_, name, *_rest) in found:
        print(f"   {s:.3f} {name}")
    print("   답:", a)
    print()