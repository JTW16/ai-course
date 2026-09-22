VRAM = 8.0   # 내 GPU의 VRAM (GB)

models = [("qwen3:1.7b", 1.7), ("qwen3:4b", 4.0), ("qwen3:8b", 8.2), ("qwen3:14b", 14.8),
          ("qwen3:32b", 32.8), ("gpt-oss:120b", 117)]

print(f"{'모델':14s} {'16비트':>8s} {'4비트':>8s}   8GB에")
for name, b in models:
    fp16 = b * 2            # 파라미터 10억 개 × 2바이트 = 2GB
    q4 = b * 0.6            # 4비트 양자화는 파라미터 10억 개당 약 0.6GB
    fits = "들어감" if q4 + 1.5 <= VRAM else "안 들어감"    # 1.5GB는 컨텍스트와 화면 출력 몫
    print(f"{name:14s} {fp16:7.1f}GB {q4:7.1f}GB   {fits}")

print("\nqwen3:8b의 컨텍스트 메모리 (토큰당 147KB)")
for ctx in [4096, 8192, 16384, 32768]:
    f16 = ctx * 147 / 1024 / 1024
    print(f"  {ctx:6d} 토큰: 16비트 {f16:4.1f}GB, 8비트(q8_0) {f16 / 2:4.1f}GB, 모델 5.2GB와 합치면 {5.2 + f16:4.1f}GB / {5.2 + f16 / 2:4.1f}GB")