from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from load import load_articles, FILES

docs = []
for f, name in FILES.items():
    docs += load_articles(f, name)
# 긴 조문은 잘라서 넣는다. metadata는 복사된다
docs = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
print("청크 수:", len(docs))
store = InMemoryVectorStore.from_documents(docs, OllamaEmbeddings(model="bge-m3"))
store.dump("rules.json")
print("저장: rules.json")