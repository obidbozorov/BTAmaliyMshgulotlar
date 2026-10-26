# 3-topshiriq: Qisqartirilgan xesh uchun kolliziya izlash
import hashlib, itertools, string, time

N = int(input("Xeshning necha belgisini olamiz? (4-7 tavsiya etiladi): "))

korilgan = {}
boshlandi = time.time()
alifbo = string.ascii_lowercase

for uzunlik in range(1, 7):
    for kombinatsiya in itertools.product(alifbo, repeat=uzunlik):
        soz = "".join(kombinatsiya)
        qisqa = hashlib.sha256(soz.encode()).hexdigest()[:N]
        if qisqa in korilgan and korilgan[qisqa] != soz:
            print(f"\nKOLLIZIYA TOPILDI!")
            print(f"  '{korilgan[qisqa]}'  va  '{soz}'")
            print(f"  ikkalasining xeshi ham '{qisqa}...' bilan boshlanadi")
            print(f"  Tekshirilgan variantlar : {len(korilgan):,}")
            print(f"  Sarflangan vaqt         : {time.time() - boshlandi:.2f} s")
            raise SystemExit
        korilgan[qisqa] = soz
