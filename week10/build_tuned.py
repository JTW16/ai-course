from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from load import load_articles, FILES

# (문서, 조문 제목): 그 조문 앞에 붙일 질문
EXTRA = {
    ("학칙", "제35조(교과이수 단위)"): "한 학기에 최대 몇 학점까지 들을 수 있어? 2년제는 졸업하려면 학점 몇 개 필요해?",
    ("학사 규정", "제4조(재입학)"): "제적되고 나서 재입학은 언제부터 신청할 수 있어?",
}
docs = []
for f, name in FILES.items():
    docs += load_articles(f, name)
for d in docs:
    q = EXTRA.get((d.metadata["source"], d.metadata["article"]))
    if q:
        d.page_content = q + "\n" + d.page_content
docs = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
InMemoryVectorStore.from_documents(docs, OllamaEmbeddings(model="bge-m3")).dump("rules_tuned.json")
print("저장: rules_tuned.json")