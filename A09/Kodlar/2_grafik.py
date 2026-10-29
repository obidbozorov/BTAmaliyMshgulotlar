# A10 · 2-skript: qiyinlik–vaqt grafigi (1_mayning.py natijasidan)
# O'rnatish: pip install matplotlib
import csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("mayning_natija.csv")))
d = [int(r["nol_bit"]) for r in rows]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
a1.semilogy(d, [float(r["kutilgan"]) for r in rows], "--", color="#8D88B5", label="Nazariy: 2^d")
a1.semilogy(d, [float(r["urinish"]) for r in rows], "o-", color="#5B4BDB", label="O'lchangan")
a1.set_xlabel("Talab qilingan nol bitlar (d)"); a1.set_ylabel("Urinishlar soni (log)"); a1.legend(); a1.grid(alpha=.3)
a2.semilogy(d, [float(r["vaqt_s"]) for r in rows], "o-", color="#F0675A")
a2.set_xlabel("Talab qilingan nol bitlar (d)"); a2.set_ylabel("Vaqt, sekund (log)"); a2.grid(alpha=.3)
fig.suptitle("PoW: har bir qo'shimcha nol bit ishni ikki barobar oshiradi")
fig.tight_layout(); fig.savefig("qiyinlik_vaqt.png", dpi=150)
print("qiyinlik_vaqt.png saqlandi")
