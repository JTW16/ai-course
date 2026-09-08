import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

docs = [
    "김치찌개는 신김치와 돼지고기를 넣고 끓인다",
    "파스타 면은 끓는 물에 소금을 넣고 삶는다",
    "빵을 구울 때는 반죽을 충분히 발효시켜야 한다",
    "커피는 원두를 갈아 뜨거운 물로 내린다",
    "생선회는 신선도가 무엇보다 중요하다",
    "떡볶이는 고추장과 설탕으로 매콤달콤하게 양념한다",
    "스테이크는 굽기 전에 실온에 미리 꺼내둔다",
    "김밥은 밥에 참기름과 소금으로 간을 한다",
    "된장국은 멸치육수에 된장을 풀어 끓인다",
    "카레는 채소와 고기를 볶은 뒤 물을 넣고 끓인다",
]
D = np.stack([emb(d) for d in docs])          # 문서 10개를 미리 벡터로 (10 x 1024)

def search(question, k=3):
    q = emb(question)
    sims = D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))   # 문서 10개와의 코사인을 한 번에
    for i in np.argsort(-sims)[:k]:
        print(f"   {sims[i]:.3f}  {docs[i]}")

for question in ["인도 요리 만드는 법 알려줄래?", "베이킹할 때 왜 시간이 오래 걸려?", "고기는 언제 냉장고에서 꺼내야 해?"]:
    print("Q:", question)
    search(question)