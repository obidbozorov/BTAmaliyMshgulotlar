"""
RIPEMD-160 amalda: ochiq kalitdan Bitcoin manzilini hosil qilish
Kerak: pip install pycryptodome
"""
from Crypto.Hash import SHA256, RIPEMD160

ALIFBO = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58(b: bytes) -> str:
    son = int.from_bytes(b, "big")
    natija = ""
    while son > 0:
        son, qoldiq = divmod(son, 58)
        natija = ALIFBO[qoldiq] + natija
    for bayt in b:                      # boshidagi har bir nol bayt -> "1"
        if bayt != 0: break
        natija = "1" + natija
    return natija

def hash160(data: bytes) -> bytes:
    """Bitcoin'ning HASH160 amali: RIPEMD160(SHA256(x))"""
    return RIPEMD160.new(SHA256.new(data).digest()).digest()

def manzil_yasa(ochiq_kalit_hex: str, versiya: int = 0x00) -> str:
    pub = bytes.fromhex(ochiq_kalit_hex)

    h160 = hash160(pub)                                   # 1) 20 baytga siqish
    versiyali = bytes([versiya]) + h160                   # 2) tarmoq belgisi
    nazorat = SHA256.new(SHA256.new(versiyali).digest()).digest()[:4]   # 3) checksum
    return base58(versiyali + nazorat)                    # 4) Base58

# --- Namuna: yopiq kalit = 1 bo'lgandagi ochiq kalit ---
toliq = ("04"
    "79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
    "483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8")
siqiq = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"

for nom, pub, kutilgan in [
    ("To'liq (65 bayt)", toliq, "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm"),
    ("Siqiq  (33 bayt)", siqiq, "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"),
]:
    h = hash160(bytes.fromhex(pub))
    m = manzil_yasa(pub)
    print(f"\n{nom}")
    print(f"  Ochiq kalit : {len(pub)//2} bayt")
    print(f"  SHA-256     : {SHA256.new(bytes.fromhex(pub)).hexdigest()}")
    print(f"  RIPEMD-160  : {h.hex()}   ({len(h)} bayt)")
    print(f"  Manzil      : {m}")
    print(f"  Kutilgan    : {kutilgan}")
    print(f"  Mos keldimi : {m == kutilgan}")
