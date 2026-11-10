import glob, os, re, sys
from docx import Document
from docx.oxml.ns import qn

for f in sorted(glob.glob(sys.argv[1] + "/**/*.docx", recursive=True)):
    d = Document(f)
    rpr = d.styles["Normal"].element.rPr
    east = rpr.rFonts.get(qn("w:eastAsia")) if rpr is not None and rpr.rFonts is not None else None
    paras = [p for p in d.paragraphs if p.text.strip()]
    styles = [p.style.name for p in paras]
    texts = [p.text for p in paras]
    heads = [t for t, s in zip(texts, styles) if s == "Heading 1"]
    conclusion = texts[texts.index(heads[-1]) + 1:] if heads else []
    checks = {
        "파일명": re.search(r"report_\d{8}\.docx$", f) is not None,
        "Title": styles[:1] == ["Title"],
        "작성일": any(t.startswith("작성일:") for t in texts),
        "절 3개": len(heads) == 3,
        "맑은 고딕": east == "맑은 고딕",
        "Table Grid": bool(d.tables) and d.tables[0].style.name == "Table Grid",
        "결론 2문장": 0 < sum(t.count(".") for t in conclusion) <= 2,
    }
    failed = " ".join(k for k, v in checks.items() if not v)
    print(f"{sum(checks.values())}/{len(checks)}", os.path.relpath(f, sys.argv[1]), failed)