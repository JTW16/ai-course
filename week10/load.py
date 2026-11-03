import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

FILES = {"hakchik.pdf": "학칙", "haksa.pdf": "학사 규정"}


def load_articles(path, name):
    pages = PyPDFLoader(path).load()
    text = "\n".join(p.page_content for p in pages)
    text = text.split("부       칙")[0]                        # 부칙과 별표는 뺀다
    text = re.sub(r"^(학칙\(02-01\)|학사 규정\(06-01\)|학칙|- \d+ -)\s*$", "", text, flags=re.M)
    # 줄 끝에서 끊긴 낱말을 이어 붙인다. 항 번호(①②…)나 호 번호(1. 2.)로 시작하는 줄은 새 줄로 둔다
    text = re.sub(r"\n(?![①-⑮]|\s*\d+\.\s|제\d+[조장])", "", text)
    docs, chapter = [], ""
    for block in re.split(r"\n(?=제\d+조(?:의\s?\d+)?\()", text):
        m = re.search(r"(제\d+장\s*\S.*)$", block)             # 블록 끝에 붙은 다음 장 제목
        if m:
            block, next_chapter = block[:m.start()].strip(), m.group(1).strip()
        else:
            next_chapter = chapter
        if block.startswith("제") and "조(" in block[:12]:
            title = block[:block.index(")") + 1]
            docs.append(Document(page_content=f"[{name} {title}] {block}",
                                 metadata={"source": name, "article": title, "chapter": chapter}))
        chapter = next_chapter
    return docs


if __name__ == "__main__":
    for f, name in FILES.items():
        docs = load_articles(f, name)
        print(name, "조문 수:", len(docs))
    print(docs[30].metadata)
    print(docs[30].page_content[:200])