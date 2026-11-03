from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

store = InMemoryVectorStore.load("rules.json", OllamaEmbeddings(model="bge-m3"))
retriever = store.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none",
                 model="gemma4", temperature=0)

rewrite = ChatPromptTemplate.from_messages([
    ("system", "대화 기록을 참고해서 마지막 질문을 기록 없이도 이해되는 독립된 한 문장으로 다시 쓴다. 질문만 출력한다."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
]) | llm | StrOutputParser()

answer = ChatPromptTemplate.from_template("""아래 규정만 근거로 질문에 답한다. 규정에 없는 내용은 "규정에 없습니다"라고 답한다. 두 문장 이내.

규정:
{context}

질문: {question}""") | llm | StrOutputParser()

history = []
for q in ["휴학은 몇 번까지 할 수 있어?", "그거 한 번에 얼마나 쉴 수 있어?", "군대 가는 것도 거기에 들어가?"]:
    standalone = rewrite.invoke({"history": history, "question": q}).strip() if history else q
    docs = retriever.invoke(standalone)
    a = answer.invoke({"context": "\n\n".join(d.page_content for d in docs),
                       "question": standalone}).strip()
    print("Q:", q)
    print("   검색용 질문:", standalone)
    print("   답:", a)
    history += [HumanMessage(q), AIMessage(a)]