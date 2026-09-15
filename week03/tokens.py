from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B")

pairs = [
    ("나는 어제 친구와 함께 영화를 봤다", "I watched a movie with a friend yesterday"),
    ("인공지능은 데이터에서 규칙을 스스로 배운다", "Artificial intelligence learns rules from data by itself"),
    ("대한민국의 수도는 서울이다", "The capital of Korea is Seoul"),
]
for ko, en in pairs:
    ki, ei = tok.encode(ko), tok.encode(en)
    print(f"한국어 {len(ki):2d} 토큰: {[tok.decode([i]) for i in ki]}")
    print(f"영어   {len(ei):2d} 토큰: {[tok.decode([i]) for i in ei]}")
    print(f"비율 {len(ki)/len(ei):.2f}\n")
print("어휘 크기:", tok.vocab_size)