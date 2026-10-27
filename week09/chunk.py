text = open("guide.txt", encoding="utf-8").read()

paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
print("문단 수:", len(paragraphs))
for i, p in enumerate(paragraphs[:6]):
    print(f"[{i}] {len(p)}자: {p[:40]}...")

# 글자 수로 자르면 문장 중간이 끊긴다
size = 200
pieces = [text[i:i + size] for i in range(0, len(text), size)]
print("\n200자 단위:", len(pieces), "조각")
print("[3]", repr(pieces[3][:60]))
print("[4]", repr(pieces[4][:60]))