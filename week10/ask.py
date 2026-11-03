import sys
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

emb = OllamaEmbeddings(model="bge-m3")
store = InMemoryVectorStore.load("rules.json", emb)
retriever = store.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none",
                 model="gemma4", temperature=0)

prompt = ChatPromptTemplate.from_template("""아래 규정만 근거로 학생의 질문에 답한다. 규정에서 추론할 수 있는 것은 답하고, 규정에 없는 내용은 "규정에 없습니다"라고 답한다. 답은 두 문장 이내로 쓰고, 근거가 된 조문 번호를 괄호에 적는다.

규정:
{context}

질문: {question}""")


def join(docs):
    return "\n\n".join(d.page_content for d in docs)


chain = ({"context": retriever | join, "question": RunnablePassthrough()}
         | prompt | llm | StrOutputParser())

questions = sys.argv[1:] or [
    "휴학은 몇 번까지 할 수 있어?",
    "수업 4분의 1 넘게 빠지면 어떻게 돼?",
    "기숙사비는 얼마야?",
]
for q in questions:
    print("Q:", q)
    for d in retriever.invoke(q):
        print(f"   {d.metadata['source']} {d.metadata['article']}")
    print("   답:", chain.invoke(q).strip())
    print()