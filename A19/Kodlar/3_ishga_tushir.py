# A19 · 3-skript: 2_sorovlar.sql dagi so'rovlarni mashq bazasida bajaradi va natijani ko'rsatadi
import duckdb, re
con = duckdb.connect("bt_mashq.duckdb", read_only=True)
matn = open("2_sorovlar.sql", encoding="utf-8").read()
for blok in re.split(r"\n(?=-- \[\d\])", matn):
    sarlavha = re.search(r"-- \[(\d)\] (.+)", blok)
    sql = "\n".join(l for l in blok.splitlines() if not l.strip().startswith("--")).strip().rstrip(";")
    if not sarlavha or not sql: continue
    df = con.execute(sql).fetchdf()
    print(f"\n[{sarlavha.group(1)}] {sarlavha.group(2)}  ({len(df)} qator)")
    print(df.head(8).to_string(index=False))
