# A20 · 2-skript: likvidlik provayderi (LP) nima oladi va nima yo'qotadi? Komissiya daromadi va doimiy bo'lmagan zarar
# Ishga tushirish: python 2_likvidlik.py
from math import sqrt
from amm import Havza

E = 10**18
print("1) LP tokenlar: havzadagi ulush")
h = Havza()
ali = h.likvidlik_qosh("Ali", 10 * E, 30_000 * E)
vali = h.likvidlik_qosh("Vali", 5 * E, 15_000 * E)
print(f"   Ali 10 ETH + 30 000 USDC → {ali / E:.6f} LP · Vali 5 ETH + 15 000 USDC → {vali / E:.6f} LP")
print(f"   Qulflangan minimal likvidlik: 1000 wei LP · Ali ulushi {ali / h.lp_jami:.2%}, Vali {vali / h.lp_jami:.2%}")

print("\n2) Komissiya daromadi: 200 ta savdo (100 ta ETH→USDC va 100 ta USDC→ETH, har biri ~1 ETH)")
k0, lp0 = h.x * h.y, h.lp_jami
for _ in range(100):
    h.almashtir(1 * E)                       # ETH sotadi
    h.almashtir(3_000 * E, a_dan_b_ga=False) # ETH sotib oladi
print(f"   k: {k0 / E**2:,.0f} → {h.x * h.y / E**2:,.0f} (komissiya havzada qolgani uchun k o'sdi)")
print(f"   1 LP token ortidagi √k: {sqrt(k0) / lp0:.4f} → {sqrt(h.x * h.y) / h.lp_jami:.4f}  (+{sqrt(h.x * h.y) / sqrt(k0) - 1:.2%})")
dx, dy = h.likvidlik_ol("Vali", vali)
print(f"   Vali chiqdi: {dx / E:.4f} ETH + {dy / E:,.2f} USDC (qo'ygani: 5 ETH + 15 000 USDC)")
print(f"   Narx {h.narx():,.2f} da qiymati: {(dx * h.narx() + dy) / E:,.2f} USDC · qo'yilgan qiymat shu narxda: {(5 * h.narx() + 15_000):,.2f}")

print("\n3) Doimiy bo'lmagan zarar (impermanent loss): narx o'zgarsa, LP “shunchaki saqlash”dan qancha kam oladi?")
print(f"{'ETH narxi':>12}{'Saqlash (HODL)':>17}{'LP pozitsiya':>15}{'Zarar':>9}{'Formula':>10}")
for r in [0.25, 0.5, 0.8, 1, 1.25, 2, 4]:
    p = Havza(); p.likvidlik_qosh("LP", 10 * E, 30_000 * E)
    yangi = 3000 * r
    # arbitrajchi havza narxini bozor narxiga yetkazadi (komissiyasiz ideal holat): x' = sqrt(k / p'), y' = sqrt(k · p')
    x, y = sqrt(p.x * p.y / yangi), sqrt(p.x * p.y * yangi)
    hodl = 10 * E * yangi + 30_000 * E
    lp = x * yangi + y
    print(f"{yangi:>12,.0f}{hodl / E:>17,.0f}{lp / E:>15,.0f}{lp / hodl - 1:>9.2%}{2 * sqrt(r) / (1 + r) - 1:>10.2%}")
