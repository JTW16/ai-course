import torch, time

print("GPU 사용 가능:", torch.cuda.is_available())
print("GPU 이름:", torch.cuda.get_device_name(0))

size = 4000                          # 4000 x 4000 크기의 행렬
a = torch.rand(size, size)           # 무작위 숫자로 채운 행렬 두 개를 만든다
b = torch.rand(size, size)

# CPU에서 행렬 곱셈 시간 측정
start = time.time()
c = a @ b                            # @ 가 행렬 곱셈 연산자
cpu_time = time.time() - start
print("CPU:", round(cpu_time, 4), "초")

# 같은 행렬을 GPU로 옮겨서 측정
a_gpu = a.to("cuda")                 # cuda가 곧 NVIDIA GPU를 뜻한다
b_gpu = b.to("cuda")
torch.cuda.synchronize()             # GPU 준비가 끝날 때까지 대기
start = time.time()
c_gpu = a_gpu @ b_gpu
torch.cuda.synchronize()             # GPU 계산이 끝날 때까지 대기
gpu_time = time.time() - start
print("GPU:", round(gpu_time, 4), "초")

print("GPU가 약", round(cpu_time / gpu_time), "배 빠름")