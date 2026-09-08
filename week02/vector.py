import ollama
import numpy as np

def emb(text):
    r = ollama.embed(model="bge-m3", input=text)
    return np.array(r.embeddings[0])

def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

v = emb("사과")
print("벡터 길이:", len(v))
print("앞 5개 값:", v[:5])

print("사과-배:", round(cos(emb("사과"), emb("배")), 3))
print("사과-자동차:", round(cos(emb("사과"), emb("자동차")), 3))

target = emb("왕") - emb("남자") + emb("여자")
candidates = ["여왕", "왕비", "왕자", "공주", "임금", "남자", "여자", "왕"]
print('"왕 - 남자 + 여자" 결과 벡터와 가까운 순서:')
for w in sorted(candidates, key=lambda w: -cos(target, emb(w))):
    print(f"  {w}  {cos(target, emb(w)):.3f}")