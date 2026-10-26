# 3-topshiriq: Nonce takrorlansa yopiq kalit qanday topiladi (Sony PS3 keysi)
# Faqat o'quv maqsadida! Ikki imzoda bir xil k ishlatilgan holat modellashtiriladi.
import hashlib, secrets
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_strings

n = SECP256k1.order
yopiq = secrets.randbelow(n - 1) + 1              # "maxfiy" kalit
sk = SigningKey.from_secret_exponent(yopiq, curve=SECP256k1)

k = secrets.randbelow(n - 1) + 1                  # XATO: bitta k ikki marta
def imzola(xabar):
    z = hashlib.sha256(xabar.encode()).digest()
    r, s = sk.sign_digest(z, k=k, sigencode=sigencode_strings)
    return int.from_bytes(z, "big"), int.from_bytes(r, "big"), int.from_bytes(s, "big")

z1, r1, s1 = imzola("1-xabar: 10 PRC o'tkazish")
z2, r2, s2 = imzola("2-xabar: 25 PRC o'tkazish")
print("r1 == r2 ?", r1 == r2, " <- bir xil r hujumchiga xatoni ko'rsatadi")

# Hujumchi faqat ochiq ma'lumotdan foydalanadi: z1, z2, r, s1, s2
k_top = ((z1 - z2) * pow(s1 - s2, -1, n)) % n
d_top = ((s1 * k_top - z1) * pow(r1, -1, n)) % n

print("\nHaqiqiy yopiq kalit :", format(yopiq, "064x"))
print("Topilgan kalit      :", format(d_top, "064x"))
print("Mos keldimi         :", d_top == yopiq)
