import ollama
import numpy as np

text = open("guide.txt", encoding="utf-8").read()
paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

# 절 제목("1. 수강 신청")은 따로 저장하지 않고 뒤따르는 문단 앞에 붙인다
chunks = []
title = ""
for p in paragraphs:
    if len(p) < 15 and p[0].isdigit():
        title = p.split(". ", 1)[1]
    else:
        chunks.append(f"[{title}] {p}" if title else p)

print("청크 수:", len(chunks))

vectors = []
for i, c in enumerate(chunks):
    v = ollama.embed(model="bge-m3", input=c).embeddings[0]
    vectors.append(v)
    print(f"\r{i + 1}/{len(chunks)}", end="")
print()

np.savez("index.npz", chunks=np.array(chunks, dtype=object), vectors=np.array(vectors, dtype=np.float32))
print("저장: index.npz")