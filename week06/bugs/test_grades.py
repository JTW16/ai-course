from grades import average, top_n, grade, pass_rate

TESTS = [
    ("average([80, 90, 100])", 90),
    ("average([])", 0),
    ("top_n([70, 95, 80, 60], 2)", [95, 80]),
    ("grade(90)", "A"),
    ("grade(80)", "B"),
    ("grade(69)", "F"),
    ("pass_rate([60, 70, 50, 90])", 75),
    ("pass_rate([])", 0),
]

failed = 0
for expr, want in TESTS:
    try:
        got = eval(expr)
    except Exception as e:
        got = f"예외 {type(e).__name__}: {e}"
    ok = got == want
    failed += not ok
    print("통과" if ok else "실패", expr, "기대", want, "실제", got)
print(f"{len(TESTS) - failed}/{len(TESTS)} 통과")