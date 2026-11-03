import sys
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from evalset import VALID, TEST

index = sys.argv[1] if len(sys.argv) > 1 else "rules.json"
k = int(sys.argv[2]) if len(sys.argv) > 2 else 1

store = InMemoryVectorStore.load(index, OllamaEmbeddings(model="bge-m3"))
retriever = store.as_retriever(search_kwargs={"k": k})


def hit_rate(dataset, show=False):
    hits = 0
    for q, want, _ in dataset:
        docs = retriever.invoke(q)
        ok = any(want in d.page_content for d in docs)
        hits += ok
        if show and not ok:
            print("  X", q, "->", docs[0].metadata["article"])
    return hits / len(dataset)


print(f"{index} k={k}  검증 {hit_rate(VALID, show=True):.2f}  테스트 {hit_rate(TEST):.2f}")