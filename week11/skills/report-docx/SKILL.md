---
name: report-docx
description: 보고서, 결과 정리, 회의록처럼 글과 표로 된 문서를 워드(docx) 파일로 만들 때 쓴다. 엑셀이나 PDF에는 쓰지 않는다.
---

# 보고서 docx 만들기

## 규칙

- 파일 이름은 `report_YYYYMMDD.docx` (오늘 날짜). 다른 이름을 쓰지 않는다.
- 문서 맨 위에 제목을 'Title' 스타일로 넣는다.
- 제목 바로 아래에 "작성일: YYYY-MM-DD" 한 줄을 넣는다.
- 절 제목은 'Heading 1' 스타일을 쓴다. 절 순서는 개요, 결과, 결론이다.
- 표는 'Table Grid' 스타일을 쓰고 첫 줄은 머리글이다.
- 본문 글꼴은 맑은 고딕 11pt다. 아래 `set_font`를 그대로 써서 문서 전체에 적용한다.
- 받은 내용을 그대로 쓴다. 문장을 늘리거나 설명을 덧붙이지 않는다.

## 코드

python-docx를 쓴다. 다음 함수를 그대로 복사해 쓴다. 한글 글꼴은 `w:eastAsia`를 따로 지정해야 바뀐다.

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

def set_font(doc, name="맑은 고딕", size=11):
    style = doc.styles["Normal"]
    style.font.name = name
    style.font.size = Pt(size)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), name)

def add_table(doc, header, rows):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, h in enumerate(header):
        t.rows[0].cells[i].text = str(h)
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = str(v)
    return t
```

저장한 뒤 `print("saved", 파일명)`으로 파일 이름을 출력한다.