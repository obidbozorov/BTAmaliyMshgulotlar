# 5-topshiriq: Bitcoin manzilining nazorat summasini tekshirish
from Crypto.Hash import SHA256
ALIFBO = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def tekshir(manzil):
    try:
        son = 0
        for c in manzil:
            son = son * 58 + ALIFBO.index(c)
    except ValueError:
        return False, "ruxsat etilmagan belgi"
    b = son.to_bytes(25, "big")
    tana, nazorat = b[:-4], b[-4:]
    kutilgan = SHA256.new(SHA256.new(tana).digest()).digest()[:4]
    return nazorat == kutilgan, "HASH160 = " + tana[1:].hex()

for m in ["1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",   # to'g'ri
          "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMJ",   # oxirgi belgi xato
          "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAM0"]:  # '0' Base58 da yo'q
    ok, izoh = tekshir(m)
    print(f"{m}  ->  {'YAROQLI' if ok else 'YAROQSIZ'}   ({izoh})")
