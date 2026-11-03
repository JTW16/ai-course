from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pages = PyPDFLoader("hakchik.pdf").load()
print("페이지 수:", len(pages))
print(pages[5].metadata)
print(pages[5].page_content[:300])

chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(pages)
print("\n청크 수:", len(chunks))
print(chunks[20].page_content)