# A22 · 2-skript: M/N sxemasi qancha xavfsiz? Kalit o'g'irlanishi va yo'qolishi ehtimoli
from math import comb

def kamida(k, n, p):                       # n tadan kamida k tasi hodisaga uchrashi ehtimoli
    return sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))

if __name__ == "__main__":
    p_ogir, p_yoq = 0.05, 0.05             # har bir kalit uchun yillik ehtimol (shartli)
    print(f"Har bir kalit: o'g'irlanish {p_ogir:.0%}, yo'qolish {p_yoq:.0%}\n")
    print(f"{'Sxema':8}{'O‘g‘irlash (M ta kalit kerak)':>32}{'Kirish yo‘qoladi':>20}")
    for m, n in [(1, 1), (1, 2), (2, 2), (2, 3), (3, 5)]:
        ogir = kamida(m, n, p_ogir)                 # hujumchi M ta kalitni olsa
        yoq = kamida(n - m + 1, n, p_yoq)           # N−M+1 ta yo'qolsa, M yig'ilmaydi
        print(f"{m}/{n:<6}{ogir:>32.4%}{yoq:>20.4%}")
