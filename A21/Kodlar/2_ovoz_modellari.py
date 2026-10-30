# A21 · 2-skript: bir xil taklif turli ovoz berish tizimlarida qanday hal bo'ladi?
# 1 a'zo = 1 ovoz (bizning DAO), token bilan vaznlangan, kvadratik ovoz va Sybil hujumi. Ishga tushirish: python 2_ovoz_modellari.py
from math import sqrt

# 10 a'zo va ularning boshqaruv tokenlari (jami 1000). “Kit” — eng ko'p tokenli a'zo
TOKENLAR = {"Kit": 400, "A1": 100, "A2": 80, "A3": 80, "A4": 70, "A5": 70, "A6": 60, "A7": 50, "A8": 50, "A9": 40}
OVOZ = {"Kit": "ha", "A1": "betaraf", "A2": "yoq", "A3": "yoq", "A4": "yoq", "A5": "yoq", "A6": "yoq", "A7": "betaraf", "A8": None, "A9": None}
KVORUM = 0.4                                          # ishtirok etgan vazn ulushi

def hisobla(vazn_fn, tokenlar=TOKENLAR, ovozlar=OVOZ):
    jami = sum(vazn_fn(t) for t in tokenlar.values())
    s = {"ha": 0.0, "yoq": 0.0, "betaraf": 0.0}
    for kim, ov in ovozlar.items():
        if ov: s[ov] += vazn_fn(tokenlar[kim])
    ishtirok = sum(s.values()) / jami
    qaror = "QABUL" if ishtirok >= KVORUM and s["ha"] > s["yoq"] else "RAD"
    return s, ishtirok, qaror

print("Taklif: “Xazinaning 30% ini Kit bergan loyihaga ajratish”. Kit — HA, 5 a'zo — YO'Q, 2 betaraf, 2 ovoz bermadi.\n")
print(f"{'Tizim':34}{'Ha':>8}{'Yo‘q':>8}{'Betaraf':>9}{'Ishtirok':>10}{'Qaror':>8}")
for nom, fn in [("1 a'zo = 1 ovoz (DAO.sol)", lambda t: 1), ("Token bilan vaznlangan (1 token = 1)", lambda t: t),
                ("Kvadratik (√token)", lambda t: sqrt(t))]:
    s, ish, q = hisobla(fn)
    print(f"{nom:34}{s['ha']:>8.1f}{s['yoq']:>8.1f}{s['betaraf']:>9.1f}{ish:>10.0%}{q:>8}")

print("\nSybil hujumi: Kit 400 tokenini 16 ta yangi manzilga bo'lib yuboradi (har biri 25 token) va hammasidan HA beradi.")
sybil_t = {k: v for k, v in TOKENLAR.items() if k != "Kit"} | {f"Kit_{i}": 25 for i in range(16)}
sybil_o = {k: v for k, v in OVOZ.items() if k != "Kit"} | {f"Kit_{i}": "ha" for i in range(16)}
for nom, fn in [("Kvadratik, Sybil'dan keyin", lambda t: sqrt(t)), ("1 manzil = 1 ovoz, tekshiruvsiz", lambda t: 1)]:
    s, ish, q = hisobla(fn, sybil_t, sybil_o)
    print(f"{nom:34}{s['ha']:>8.1f}{s['yoq']:>8.1f}{s['betaraf']:>9.1f}{ish:>10.0%}{q:>8}")
print("\nMerkle ro'yxati (A3) Sybil'dan himoya qiladi: yangi manzil ro'yxatda yo'q, root'ni faqat yangi DAO qarori o'zgartiradi.")

print("\nKvorum ta'siri (1 a'zo = 1 ovoz): faqat k ta a'zo ovoz bersa va hammasi HA desa")
for k in [2, 3, 4, 5]:
    s, ish, q = hisobla(lambda t: 1, ovozlar={kim: ("ha" if i < k else None) for i, kim in enumerate(TOKENLAR)})
    print(f"   {k} ta ovoz → ishtirok {ish:.0%} → {q}")
