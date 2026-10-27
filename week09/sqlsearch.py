import sqlite3

con = sqlite3.connect("campus.db")
for kw in ["출력", "밤", "공부", "차"]:
    rows = con.execute("SELECT name FROM facility WHERE name LIKE ? OR description LIKE ?",
                       (f"%{kw}%", f"%{kw}%")).fetchall()
    print(kw, [r[0] for r in rows])