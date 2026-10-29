# A7 · 4-skript: Bitcoin komissiyasi — narx “sat/vB” da, miqdorga emas, hajmga bog'liq
# SegWit (P2WPKH) tranzaksiya hajmi uchun taxminiy formula: 10,5 + 68·kirish + 31·chiqish vbayt
def vhajm(kirish, chiqish):
    return 10.5 + 68 * kirish + 31 * chiqish

if __name__ == "__main__":
    BTC_USD = 100_000                                 # hisob uchun shartli kurs
    print(f"{'Tranzaksiya':28}{'vB':>8}{'2 sat/vB':>12}{'20 sat/vB':>12}{'100 sat/vB':>12}")
    for nom, k, c in [("1 kirish → 2 chiqish", 1, 2), ("3 kirish → 2 chiqish", 3, 2), ("1 kirish → 10 chiqish", 1, 10), ("20 kirish → 1 chiqish", 20, 1)]:
        v = vhajm(k, c)
        narx = [f"${v*s/1e8*BTC_USD:,.2f}" for s in (2, 20, 100)]
        print(f"{nom:28}{v:>8.1f}{narx[0]:>12}{narx[1]:>12}{narx[2]:>12}")
    print("\n0,001 BTC ham, 100 BTC ham 1→2 tranzaksiyada bir xil komissiya to'laydi.")
