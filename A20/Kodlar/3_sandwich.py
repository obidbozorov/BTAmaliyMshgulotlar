# A20 · 3-skript: “sendvich” hujumi (MEV) — slippage chegarasi qanchalik muhim?
# Hujumchi mempool'da qurbon tranzaksiyasini ko'radi: oldidan sotib oladi, keyin qimmatga sotadi. Ishga tushirish: python 3_sandwich.py
from amm import Havza, Rad

E = 10**18
QURBON = 10_000 * E                    # qurbon 10 000 USDC ga ETH sotib oladi

def sinov(slippage, hujum_usdc):
    h = Havza(); h.likvidlik_qosh("LP", 100 * E, 300_000 * E)
    kutilgan = Havza(); kutilgan.likvidlik_qosh("LP", h.x, h.y)
    halol = kutilgan.almashtir(QURBON, a_dan_b_ga=False)
    minimal = int(halol * (1 - slippage))
    eth = h.almashtir(hujum_usdc, a_dan_b_ga=False) if hujum_usdc else 0      # 1) front-run: ETH sotib oladi
    try:
        olindi = h.almashtir(QURBON, a_dan_b_ga=False, min_chiqish=minimal)  # 2) qurbon tranzaksiyasi
    except Rad:
        return None
    qaytdi = h.almashtir(eth, a_dan_b_ga=True) if eth else 0               # 3) back-run: ETH ni sotadi
    return halol, olindi, qaytdi - hujum_usdc

def eng_yaxshi_hujum(slippage):
    eng = (0, 0, None)
    for usdc in range(0, 200_001, 250):                      # hujumchi eng foydali hajmni qidiradi
        r = sinov(slippage, usdc * E)
        if r and r[2] > eng[1]: eng = (usdc, r[2], r)
    return eng

print(f"Qurbon {QURBON / E:,.0f} USDC ga ETH sotib oladi. Havza 100 ETH / 300 000 USDC.\n")
print(f"{'Slippage':>9}{'Hujum, USDC':>13}{'Qurbon oladi, ETH':>19}{'Hujumsiz, ETH':>15}{'Qurbon zarari':>15}{'Hujumchi foydasi':>18}")
for s in [0.001, 0.005, 0.01, 0.03, 0.05, 0.10]:
    usdc, foyda, r = eng_yaxshi_hujum(s)
    if not r:
        print(f"{s:>9.1%}{'—':>13}{'hujum foydasiz':>19}"); continue
    halol, olindi, _ = r
    print(f"{s:>9.1%}{usdc:>13,}{olindi / E:>19.4f}{halol / E:>15.4f}{(halol - olindi) / halol:>15.2%}{'$' + format(foyda / E, ',.2f'):>18}")
print("\nGaz xarajati hisobga olinmagan. Himoya: past slippage, private mempool (Flashbots Protect), kichik bo'laklarga bo'lish.")
