# 3-topshiriq: Guruh ro'yxatidan Merkle daraxti va proof
# Kerak: pip install pycryptodome
from Crypto.Hash import keccak

def kek(b):
    h = keccak.new(digest_bits=256); h.update(b); return h.digest()

def barg(manzil):
    """Solidity'dagi keccak256(bytes.concat(keccak256(abi.encode(addr)))) bilan bir xil"""
    addr = bytes.fromhex(manzil[2:].lower())
    return kek(kek(bytes(12) + addr))          # abi.encode: 32 baytgacha chapdan to'ldiriladi

def juft(a, b):
    return kek(a + b) if a < b else kek(b + a)  # OpenZeppelin tartiblangan juftlik

def daraxt_qur(barglar):
    darajalar = [barglar]
    while len(darajalar[-1]) > 1:
        joriy = darajalar[-1]; keyingi = []
        for i in range(0, len(joriy), 2):
            keyingi.append(juft(joriy[i], joriy[i+1]) if i+1 < len(joriy) else joriy[i])
        darajalar.append(keyingi)
    return darajalar

def proof_ol(darajalar, indeks):
    proof = []
    for d in darajalar[:-1]:
        juftindeks = indeks ^ 1
        if juftindeks < len(d):
            proof.append(d[juftindeks])
        indeks //= 2
    return proof

def tekshir(bargim, proof, ildiz):
    hozir = bargim
    for p in proof:
        hozir = juft(hozir, p)
    return hozir == ildiz

# --- Guruh ro'yxati (o'z guruhingiz manzillari bilan almashtiring) ---
guruh = [
    "0x2c7536e3605d9c16a7a3d7b1898e529396a65c23",
    "0x7e5f4552091a69125d5dfcb7b8c2659029395bdf",
    "0x2b5ad5c4795c026514f8317c7a215e218dccd6cf",
    "0x6813eb9362372eef6200f3b1dbc3f819671cba69",
    "0x1eff47bc3a10a45d4b230b5d10e37751fe6aa718",
    "0xe1ab8145f7e55dc933d51a18c793f901a3a0b276",
]

barglar   = [barg(m) for m in guruh]
darajalar = daraxt_qur(barglar)
ildiz     = darajalar[-1][0]

print("Ro'yxatdagi manzillar :", len(guruh))
print("Daraxt balandligi     :", len(darajalar) - 1)
print("MERKLE ROOT           : 0x" + ildiz.hex())

n = 1   # o'z tartib raqamingiz
print(f"\n--- {n}-manzil uchun proof ---")
print("Manzil :", guruh[n])
p = proof_ol(darajalar, n)
print("Proof  :", len(p), "ta xesh")
for x in p:
    print("   0x" + x.hex())
print("Tekshiruv natijasi :", tekshir(barglar[n], p, ildiz))

# --- Ro'yxatda yo'q manzil bilan sinov ---
begona = "0x000000000000000000000000000000000000dead"
print("\n--- Ro'yxatda yo'q manzil ---")
print("Manzil :", begona)
print("Tekshiruv natijasi :", tekshir(barg(begona), p, ildiz))

# --- Natijani JSON faylga saqlash (A22 mashg'ulotigacha saqlang!) ---
import json
with open("mening_proofim.json", "w", encoding="utf-8") as f:
    json.dump({
        "manzil": guruh[n],
        "indeks": n,
        "root":   "0x" + ildiz.hex(),
        "proof":  ["0x" + x.hex() for x in p],
    }, f, indent=2)
print("\nSaqlandi: mening_proofim.json")
