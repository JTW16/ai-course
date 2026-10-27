import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
columns = [c[1] for c in con.execute("PRAGMA table_info(facility)")]
if "embedding" not in columns:
    con.execute("ALTER TABLE facility ADD COLUMN embedding BLOB")


def row_to_text(name, area, walk_min, hours, category, description):
    # 7번 실험: 설명을 앞에 두고 위치·시간은 뒤로 (전: 이름. 위치. 분류. 영업시간. 설명)
    return f"{name}. {category}. {description}. {area}, 집에서 걸어서 {walk_min}분. 영업시간 {hours}"


rows = con.execute("SELECT id, name, area, walk_min, hours, category, description FROM facility").fetchall()
for i, (id_, *fields) in enumerate(rows):
    text = row_to_text(*fields)
    v = np.array(ollama.embed(model="bge-m3", input=text).embeddings[0], dtype=np.float32)
    con.execute("UPDATE facility SET embedding = ? WHERE id = ?", (v.tobytes(), id_))
    print(f"\r{i + 1}/{len(rows)} {text[:40]}", end="   ")
con.commit()
print("\n완료")
print("예:", row_to_text(*rows[0][1:]))