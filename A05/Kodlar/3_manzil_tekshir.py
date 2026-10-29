# A5 · 3-skript: manzilni nusxalashda xato bormi? EIP-55 nazorat summasi
# O'rnatish: pip install pycryptodome
import sys
from Crypto.Hash import keccak

def eip55(manzil: str) -> str:
    a = manzil.lower().replace("0x", "")
    h = keccak.new(digest_bits=256); h.update(a.encode()); hx = h.hexdigest()
    return "0x" + "".join(c.upper() if int(hx[i], 16) >= 8 else c for i, c in enumerate(a))

def tekshir(manzil: str) -> str:
    a = manzil.replace("0x", "")
    if len(a) != 40 or any(c not in "0123456789abcdefABCDEF" for c in a):
        return "YAROQSIZ: 40 ta 16-lik belgi bo'lishi kerak"
    if a == a.lower() or a == a.upper():
        return "OGOHLANTIRISH: katta-kichik harf yo'q — nazorat summasini tekshirib bo'lmaydi"
    return "TO'G'RI ✓" if eip55(manzil) == "0x" + a else "XATO: nazorat summasi mos emas — manzil buzilgan!"

if __name__ == "__main__":
    namunalar = sys.argv[1:] or [
        "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",   # to'g'ri
        "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92267",   # oxirgi belgi o'zgargan
        "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266",   # hammasi kichik harf
    ]
    for m in namunalar:
        print(m, "→", tekshir(m))
