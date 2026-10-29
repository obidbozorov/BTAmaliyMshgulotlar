# A12 · 1-skript: Dune'dagi ethereum.transactions jadvaliga o'xshash mashq bazasini yaratadi
# Ma'lumotlar SUN'IY (tasodifiy) — SQL'ni oflayn mashq qilish uchun. O'rnatish: pip install duckdb
import duckdb, random, datetime

random.seed(42)
MANZILLAR = [f"0x{random.getrandbits(160):040x}" for _ in range(300)]
BIRJA = "0x" + "be" * 20                     # “faol” manzil — ko'p tranzaksiya yuboradi
boshi = datetime.datetime(2026, 9, 1)
qatorlar = []
for kun in range(30):
    soni = random.randint(800, 1200) + (400 if kun % 7 in (1, 2) else 0)   # hafta o'rtasida faolroq
    for _ in range(soni):
        vaqt = boshi + datetime.timedelta(days=kun, seconds=random.randint(0, 86399))
        kimdan = BIRJA if random.random() < 0.08 else random.choice(MANZILLAR)
        gaz = random.choice([21000] * 6 + [46000, 65000, 120000, 180000])
        narx = int(random.lognormvariate(0, 0.6) * 1e9 * (2 if kun >= 20 else 1))   # 20-kundan narx oshgan
        qatorlar.append((vaqt, 23_000_000 + kun * 7200 + random.randint(0, 7199), kimdan, random.choice(MANZILLAR),
                         int(random.expovariate(1 / 0.3) * 1e18), gaz, narx, random.random() > 0.02))
con = duckdb.connect("bt_mashq.duckdb")
con.execute('DROP TABLE IF EXISTS ethereum_transactions')
con.execute('''CREATE TABLE ethereum_transactions (block_time TIMESTAMP, block_number BIGINT, "from" VARCHAR, "to" VARCHAR,
               value DOUBLE, gas_used BIGINT, gas_price BIGINT, success BOOLEAN)''')
con.executemany("INSERT INTO ethereum_transactions VALUES (?,?,?,?,?,?,?,?)", qatorlar)
print("Yaratildi:", con.execute("SELECT count(*) FROM ethereum_transactions").fetchone()[0], "qator → bt_mashq.duckdb")
