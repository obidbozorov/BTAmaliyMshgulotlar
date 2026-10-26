"""A11 | Vaznli qaror matritsasi: ballar O'QUV EKSPERT BAHOSI, universal fakt emas."""

MEZONLAR = ["Energiya", "Finality", "Ochiqlik", "Tezlik", "Nosozlikka chidamlilik"]
# 1=yomonroq, 5=yaxshiroq (barcha mezonda yuqori ball yaxshiroq)
BALLAR = {
    "PoW":  [1, 2, 5, 2, 4],
    "PoS":  [5, 4, 5, 4, 4],
    "PoA":  [5, 4, 2, 5, 3],
    "PBFT": [4, 5, 2, 5, 4],
    "Raft": [5, 5, 1, 5, 2],
}

def reyting(vazn):
    assert len(vazn) == len(MEZONLAR) and abs(sum(vazn)-1)<1e-9
    return sorted(((sum(x*w for x,w in zip(ball, vazn)), nom)
                  for nom,ball in BALLAR.items()),reverse=True)

if __name__ == "__main__":
    holatlar = {
        "Ochiq kripto tarmoq": [0.10, 0.20, 0.40, 0.10, 0.20],
        "Korporativ reyestr":  [0.10, 0.30, 0.05, 0.25, 0.30],
        "Kam quvvatli tizim":  [0.45, 0.15, 0.10, 0.15, 0.15],
    }
    for nom, vazn in holatlar.items():
        print("\n",nom)
        for score, tex in reyting(vazn):
            print(f"  {tex:5s}: {score:.2f} / 5.00")
    print("\nVaznlar va ballarni o'zgartiring: lider o'zgaradimi?")
