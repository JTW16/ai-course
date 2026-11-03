from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

store = InMemoryVectorStore.load("rules.json", OllamaEmbeddings(model="bge-m3"))
retriever = store.as_retriever(search_kwargs={"k": 1})
llm = ChatOpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none",
                 model="gemma4", temperature=0)

grade = ChatPromptTemplate.from_template(
    "규정이 질문에 답하는 데 쓸 수 있으면 yes, 아니면 no 한 단어만 출력한다.\n\n규정:\n{context}\n\n질문: {question}"
) | llm | StrOutputParser()
rewrite = ChatPromptTemplate.from_template(
    "다음 질문을 학칙에서 찾기 쉬운 공식적인 표현으로 다시 쓴다. 질문만 출력한다.\n\n{question}"
) | llm | StrOutputParser()
answer = ChatPromptTemplate.from_template(
    "아래 규정만 근거로 질문에 두 문장 이내로 답한다.\n\n규정:\n{context}\n\n질문: {question}"
) | llm | StrOutputParser()


class State(TypedDict):
    question: str
    query: str
    context: str
    relevant: bool
    tries: int
    answer: str


def retrieve(s):
    docs = retriever.invoke(s["query"])
    return {"context": "\n\n".join(d.page_content for d in docs), "tries": s["tries"] + 1}


def check(s):
    v = grade.invoke({"context": s["context"], "question": s["question"]}).strip().lower()
    print(f"   [검색 {s['tries']}회] 질의: {s['query']} -> 판정: {v}")
    return {"relevant": v.startswith("yes")}


def route(s):
    if s["relevant"]:
        return "answer"
    return "rewrite" if s["tries"] < 2 else "giveup"


def do_rewrite(s):
    return {"query": rewrite.invoke({"question": s["question"]}).strip()}


def do_answer(s):
    return {"answer": answer.invoke({"context": s["context"], "question": s["question"]}).strip()}


def giveup(s):
    return {"answer": "규정에 없습니다."}


g = StateGraph(State)
g.add_node("retrieve", retrieve)
g.add_node("check", check)
g.add_node("rewrite", do_rewrite)
g.add_node("answer", do_answer)
g.add_node("giveup", giveup)
g.add_edge(START, "retrieve")
g.add_edge("retrieve", "check")
g.add_conditional_edges("check", route, {"answer": "answer", "rewrite": "rewrite", "giveup": "giveup"})
g.add_edge("rewrite", "retrieve")
g.add_edge("answer", END)
g.add_edge("giveup", END)
app = g.compile()

for q in ["한 학기에 최대 몇 학점까지 들을 수 있어?", "2년제는 졸업하려면 학점 몇 개 필요해?",
          "제적되고 나서 재입학은 언제부터 신청할 수 있어?", "학교 식당 밥값 얼마야?"]:
    print("Q:", q)
    r = app.invoke({"question": q, "query": q, "tries": 0})
    print("   답:", r["answer"])