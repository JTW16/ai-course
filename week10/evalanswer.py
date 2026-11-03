import sys
import time
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from evalset import TEST

name = sys.argv[1] if len(sys.argv) > 1 else "gemma4"
if name == "gemma4":
    llm = ChatOpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none", model="gemma4", temperature=0)
else:
    llm = ChatOllama(model=name, temperature=0, reasoning=False)

store = InMemoryVectorStore.load("rules.json", OllamaEmbeddings(model="bge-m3"))
retriever = store.as_retriever(search_kwargs={"k": 3})
prompt = ChatPromptTemplate.from_template("""아래 규정만 근거로 학생의 질문에 답한다. 규정에서 추론할 수 있는 것은 답하고, 규정에 없는 내용은 "규정에 없습니다"라고 답한다. 답은 두 문장 이내로 쓰고, 근거가 된 조문 번호를 괄호에 적는다.

규정:
{context}

질문: {question}""")
chain = ({"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
          "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())

ok_count, t0 = 0, time.time()
for q, _, keywords in TEST:
    a = chain.invoke(q).strip()
    ok = any(kw in a for kw in keywords)
    ok_count += ok
    print("O" if ok else "X", q, "->", a.replace("\n", " ")[:90])
print(f"\n[{name}] 정답 {ok_count}/{len(TEST)}, 질문당 {(time.time() - t0) / len(TEST):.1f}초")