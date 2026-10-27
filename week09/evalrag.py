import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
rows = con.execute("SELECT id, name, embedding FROM facility").fetchall()
names = [r[1] for r in rows]
V = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# (질문, 정답 식당 이름)
TESTS = [
    ("새벽에 해장할 데 있어?", "24시 뼈해장국"),
    ("노트북 들고 오래 앉아 있을 데?", "2층 카페"),
    ("고기 실컷 먹고 싶은데 차 가져가도 돼?", "무한리필 고기집"),
    ("집에서 짜장면 시켜 먹고 싶어", "호계반점"),
    ("아침에 갓 구운 빵 사러 갈 데", "호계 베이커리"),
    ("매운 거 내 마음대로 골라 담는 데", "마라 공방"),
    ("속 안 좋을 때 먹을 거", "본죽집"),
    ("저녁 반찬 사 갈 데", "반찬가게"),
    ("파전에 막걸리 한잔하고 싶어", "시장 전집"),
    ("평일 점심 싸게 이것저것 골라 먹을 데", "한식뷔페"),
]

hit1 = hit3 = 0
for q, want in TESTS:
    qv = np.array(ollama.embed(model="bge-m3", input=q).embeddings[0])
    qv = qv / np.linalg.norm(qv)
    top = [names[i] for i in np.argsort(-(V @ qv))[:3]]
    ok1, ok3 = top[0] == want, want in top
    hit1 += ok1
    hit3 += ok3
    print("O" if ok1 else ("△" if ok3 else "X"), q, "->", top[0], "" if ok1 else f"(정답 {want}, 3위 안 {ok3})")
print(f"\n1위 적중 {hit1}/{len(TESTS)}, 3위 안 적중 {hit3}/{len(TESTS)}")