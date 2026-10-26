# 2-topshiriq: Real Bitcoin blokining Merkle root'ini qayta hisoblash
# Blok #170 — Bitcoin tarixidagi birinchi shaxslararo to'lov (Satoshi -> Hal Finney)
import hashlib

def sha256d(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

# Blokdagi tranzaksiya identifikatorlari (explorer'da ko'rsatilgan tartibda)
txid = [
    "b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082",  # coinbase
    "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16",  # Satoshi -> Hal Finney
]

# Bitcoin ichkarida baytlarni teskari tartibda saqlaydi
daraja = [bytes.fromhex(t)[::-1] for t in txid]
print("Barglar soni:", len(daraja))

qadam = 0
while len(daraja) > 1:
    if len(daraja) % 2 == 1:          # toq bo'lsa, oxirgisi o'zi bilan juftlanadi
        daraja.append(daraja[-1])
    keyingi = []
    for i in range(0, len(daraja), 2):
        keyingi.append(sha256d(daraja[i] + daraja[i + 1]))
    daraja = keyingi
    qadam += 1
    print(f"  {qadam}-daraja: {len(daraja)} ta tugun")

hisoblangan = daraja[0][::-1].hex()
kutilgan    = "7dac2c5666815c17a3b36427de37bb9d2e2c5ccec3f8633eb91a4205cb4c10ff"

print("\nHisoblangan Merkle root:", hisoblangan)
print("Blok header'dagi qiymat:", kutilgan)
print("Mos keldimi            :", hisoblangan == kutilgan)
