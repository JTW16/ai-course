---
name: grade-xlsx
description: 이름과 점수가 있는 명단을 엑셀(xlsx) 성적표로 만들 때 쓴다. 평균과 등급 계산을 포함한다. 워드 문서에는 쓰지 않는다.
---

# 성적표 xlsx 만들기

## 규칙

- 파일 이름은 `grades_YYYYMMDD.xlsx` (오늘 날짜).
- 시트 이름은 "성적".
- 1행은 머리글: 이름, 과목별 점수 열, 평균, 등급. 머리글은 굵게.
- 평균은 소수 첫째 자리까지 반올림한다.
- 등급은 평균 90 이상 A, 80 이상 B, 70 이상 C, 그 외 F.
- 마지막 행 아래 한 줄 띄우고 "반 평균"과 전체 평균을 쓴다.
- 평균과 등급은 값으로 넣지 말고 엑셀 수식으로 넣는다. 예: `=ROUND(AVERAGE(B2:D2),1)`, `=IF(E2>=90,"A",IF(E2>=80,"B",IF(E2>=70,"C","F")))`

## 코드

openpyxl을 쓴다.

```python
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active
ws.title = "성적"
ws.append(["이름", "국어", "영어", "수학", "평균", "등급"])
for c in ws[1]:
    c.font = Font(bold=True)
```

저장한 뒤 `print("saved", 파일명)`으로 파일 이름을 출력한다.