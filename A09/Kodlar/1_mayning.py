# A10 · 1-skript: PoW mayning modeli — nonce qidiruvi va qiyinlik ta'siri
import hashlib, time, csv, statistics

def xesh(sarlavha: str, nonce: int) -> int:
    d = f"{sarlavha}|{nonce}".encode()
    return int.from_bytes(hashlib.sha256(hashlib.sha256(d).digest()).digest(), "big")

def mayn(sarlavha: str, nol_bit: int):
    maqsad = 1 << (256 - nol_bit)                  # xesh < maqsad ⇔ boshida kamida nol_bit ta nol
    t0, nonce = time.perf_counter(), 0
    while xesh(sarlavha, nonce) >= maqsad:
        nonce += 1
    return nonce + 1, time.perf_counter() - t0      # urinishlar soni, sekund

if __name__ == "__main__":
    natija = []
    print(f"{'Nol bit':>8}{'Kutilgan 2^d':>14}{'O‘rtacha urinish':>18}{'O‘rtacha vaqt, s':>18}")
    for d in range(8, 21, 2):
        takror = 5 if d <= 16 else 3
        u, v = zip(*(mayn(f"PROFI blok #{d}-{k}", d) for k in range(takror)))
        natija.append((d, 2**d, statistics.mean(u), statistics.mean(v)))
        print(f"{d:>8}{2**d:>14,}{statistics.mean(u):>18,.0f}{statistics.mean(v):>18.3f}")
    with open("mayning_natija.csv", "w", newline="") as f:
        csv.writer(f).writerows([("nol_bit", "kutilgan", "urinish", "vaqt_s"), *natija])
    tezlik = sum(r[2] for r in natija) / sum(r[3] for r in natija)
    print(f"\nKompyuteringiz tezligi ≈ {tezlik:,.0f} xesh/s")
    print(f"Bitcoin genezis bloki qiyinligi (32 nol bit) ≈ {2**32/tezlik/3600:,.1f} soat shu kompyuterda")
