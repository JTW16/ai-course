---
name: roster-csv
description: 이름, 학번, 연락처가 뒤섞인 명단을 정리해 CSV 파일로 만들 때 쓴다. 중복 제거, 정렬, 전화번호 형식 통일을 포함한다. 점수 성적표(엑셀)나 워드 문서에는 쓰지 않는다.
---

# 명단 정리 csv 만들기

## 규칙

- 파일 이름은 `roster_YYYYMMDD.csv` (오늘 날짜). 다른 이름을 쓰지 않는다.
- 인코딩은 `utf-8-sig`로 저장한다. 그래야 엑셀에서 한글이 깨지지 않는다.
- 1행은 머리글로 정확히 `번호,학번,이름,학과,전화번호` 다섯 열이다.
- 학번이 같은 사람은 한 번만 남긴다(처음 나온 줄을 남긴다).
- 학번 오름차순으로 정렬한 뒤 번호를 1부터 다시 매긴다.
- 학번은 숫자 9자리 문자열로 둔다.
- 전화번호는 숫자만 뽑아 `010-1234-5678` 꼴로 통일한다. 숫자가 11자리가 아니면 빈칸으로 둔다.
- 이름과 학과 앞뒤 공백은 지운다. 받은 내용 말고 다른 사람이나 열을 지어내지 않는다.

## 코드

표준 라이브러리 csv, re, datetime을 쓴다. 다음 함수를 그대로 복사해 쓴다.

```python
import csv, re
from datetime import date

def fmt_phone(s):
    d = re.sub(r"\D", "", s or "")
    return f"{d[:3]}-{d[3:7]}-{d[7:]}" if len(d) == 11 else ""

def save_roster(rows):
    """rows: [(학번, 이름, 학과, 전화번호), ...]"""
    seen, clean = set(), []
    for sid, name, dept, phone in rows:
        sid = re.sub(r"\D", "", str(sid))
        if sid in seen:
            continue
        seen.add(sid)
        clean.append((sid, name.strip(), dept.strip(), fmt_phone(phone)))
    clean.sort(key=lambda r: r[0])
    fn = f"roster_{date.today():%Y%m%d}.csv"
    with open(fn, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["번호", "학번", "이름", "학과", "전화번호"])
        for i, r in enumerate(clean, 1):
            w.writerow([i, *r])
    return fn
```

저장한 뒤 `print("saved", 파일명)`으로 파일 이름을 출력하고, 파일 내용을 한 번 읽어 출력해 확인한다.
