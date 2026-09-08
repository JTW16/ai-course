import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

base = "나는 어제 친구와 함께 영화를 봤다"
others = [
    "I watched a movie with a friend yesterday",
    "昨日友達と一緒に映画を見た",
    "我昨天和朋友一起看了电影",
    "어제 친구랑 영화 봤어",
    "나는 내일 혼자 도서관에 간다",
    "The weather is nice today",
]
b = emb(base)
for t in others:
    print(f"{cos(b, emb(t)):.3f}  {t}")
    