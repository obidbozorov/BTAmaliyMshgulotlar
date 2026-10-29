# A20 · 1-skript: narx qanday shakllanadi? Savdo hajmi oshgani sari narxga ta'sir (price impact)
# Havza: 100 ETH va 300 000 USDC (narx 1 ETH = 3000 USDC — shartli). Ishga tushirish: python 1_almashinuv.py
from amm import Havza, Rad

E = 10**18
h = Havza(); h.likvidlik_qosh("LP", 100 * E, 300_000 * E)
print(f"Havza: {h.x / E:,.0f} ETH / {h.y / E:,.0f} USDC · k = x·y = {h.x * h.y / E**2:,.0f} · spot narx {h.narx():,.2f}\n")
print(f"{'Sotiladi, ETH':>14}{'Olinadi, USDC':>16}{'O‘rtacha narx':>15}{'Narxga ta’sir':>15}{'Keyin spot':>12}")
for eth in [0.1, 1, 5, 10, 25, 50]:
    sinov = Havza(); sinov.likvidlik_qosh("LP", h.x, h.y)
    olindi = sinov.almashtir(int(eth * E))
    ortacha = olindi / (eth * E)
    print(f"{eth:>14}{olindi / E:>16,.2f}{ortacha:>15,.2f}{(ortacha / h.narx() - 1):>15.2%}{sinov.narx():>12,.2f}")

kutilgan = Havza(); kutilgan.likvidlik_qosh("LP", h.x, h.y)
minimal = kutilgan.almashtir(10 * E) * 99 // 100           # 1% slippage chegarasi
print(f"\nSlippage himoyasi: foydalanuvchi 10 ETH sotadi, kamida {minimal / E:,.0f} USDC (−1%) kutadi.")
sinov = Havza(); sinov.likvidlik_qosh("LP", h.x, h.y)
sinov.almashtir(5 * E)                                     # undan oldin kimdir 5 ETH sotib yubordi
try:
    sinov.almashtir(10 * E, min_chiqish=minimal)
except Rad as e:
    print(f"  Natija: rad etildi — {e}. Tranzaksiya bekor, foydalanuvchi faqat gaz yo'qotdi.")
