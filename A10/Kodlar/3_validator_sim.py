"""A11 | Bir yillik validator faoliyatini tasodifiy modellashtirish.
O'quv model: ETH protokolining epoch/slot reward qoidalari to'liq aks etmaydi.
"""
import random

KUNLAR = 365
KUNLIK_BAZA = 32*0.03/KUNLAR   # 3% shartli nominal mukofot
KUNLIK_JARIMA = KUNLIK_BAZA     # shartli: offline bo'lsa kunlik mukofot miqdorida penalty

def sinov(online_ehtimoli, seed=2026):
    rng = random.Random(seed)
    online_soni = sum(rng.random()<online_ehtimoli for _ in range(KUNLAR))
    offline_soni = KUNLAR - online_soni
    total = online_soni*KUNLIK_BAZA - offline_soni*KUNLIK_JARIMA
    return online_soni, offline_soni, round(total, 5)

if __name__ == '__main__':
    print("Stsenariy | online kun | offline kun | reward - penalty (ETH)")
    for p in [0.999, 0.98, 0.90, 0.75]:
        days_on,days_off,net=sinov(p)
        print(f"{p:7.1%}   | {days_on:10} | {days_off:11} | {net:8.5f}")
    print("Seed bir xil -> har ishga tushirishda natija takrorlanadi.")
