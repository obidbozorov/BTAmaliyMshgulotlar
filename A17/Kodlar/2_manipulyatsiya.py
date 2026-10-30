# A17 · 2-skript: nima uchun DEX'dagi joriy narxni oracle sifatida ishlatish xavfli? (flash loan hujumi modeli)
# Butunlay oflayn, sun'iy sonlar. Ishga tushirish: python 2_manipulyatsiya.py
FEE = 0.003                   # DEX komissiyasi 0,3% (A20 da batafsil)
FLASH_FEE = 0.0009            # flash loan komissiyasi 0,09%
LTV = 0.75                    # kredit protokoli: garov qiymatining 75% igacha qarz beradi

def almashtir(kirish, x, y):
    """x*y = k havzasi: y tokenidan `kirish` beradi, x tokenidan qancha olishini qaytaradi"""
    k = kirish * (1 - FEE)
    chiqish = x * k / (y + k)
    return chiqish, x - chiqish, y + kirish

X, Y = 1_000.0, 100_000.0             # havza: 1000 X token va 100 000 USDC → narx $100
garov = 10.0                          # hujumchining 10 X garovi (haqiqiy qiymati $1000)
qarz_olish = 300_000.0                # flash loan: bir tranzaksiya ichida olib-qaytariladigan USDC

print(f"Boshlang'ich: havza {X:,.0f} X / {Y:,.0f} USDC → narx ${Y / X:,.2f}")
olingan_x, x1, y1 = almashtir(qarz_olish, X, Y)
spot = y1 / x1
print(f"Hujumchi {qarz_olish:,.0f} USDC bilan {olingan_x:,.1f} X sotib oldi → joriy narx ${spot:,.2f} ({spot / (Y / X):.1f}×)")

BLOK, TWAP_BLOK = 12, 150             # 30 daqiqalik TWAP = 150 blok, manipulyatsiya faqat 1 blok davom etadi
oracles = {
    "Joriy narx (spot)": spot,
    "TWAP, 30 daqiqa": ((TWAP_BLOK - 1) * (Y / X) + spot) / TWAP_BLOK,
    "5 manba medianasi": sorted([100.2, 99.8, spot, 100.1, 99.9])[2],    # bitta manba buzilgan
}
qaytgan_usdc, _, _ = almashtir(olingan_x, y1, x1)         # X ni havzaga qaytarib sotadi
xarajat = (qarz_olish - qaytgan_usdc) + qarz_olish * FLASH_FEE
print(f"X ni qaytarib sotdi: {qaytgan_usdc:,.0f} USDC qaytdi · savdo va flash loan xarajati: ${xarajat:,.0f}\n")

print(f"{'Oracle turi':22}{'Garov narxi':>13}{'Olingan qarz':>15}{'Hujumchi foydasi':>18}{'Protokol zarari':>17}")
for nom, narx in oracles.items():
    qarz = garov * narx * LTV
    foyda = qarz - garov * (Y / X) - xarajat           # garovni tashlab ketadi: u qarzdan arzon
    zarar = max(qarz - garov * (Y / X), 0)
    print(f"{nom:22}{'$' + format(narx, ',.2f'):>13}{'$' + format(qarz, ',.0f'):>15}{'$' + format(foyda, ',.0f'):>18}{'$' + format(zarar, ',.0f'):>17}")
print("\nXulosa: foyda musbat bo'lgan oracle — hujumga ochiq. Real misollar: bZx (2020), Mango Markets (2022, ~$114 mln).")
