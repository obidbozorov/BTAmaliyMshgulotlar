# 2-topshiriq: Xabarni imzolash va tekshirish (Ethereum personal_sign formati)
# Natijani etherscan.io/verifiedSignatures sahifasida tekshirish mumkin
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
from ecdsa.util import sigencode_string, sigdecode_string
from Crypto.Hash import keccak

def kek(b):
    h = keccak.new(digest_bits=256); h.update(b); return h.digest()

def eip191(xabar: str) -> bytes:
    """Hamyonlar imzolaydigan ko'rinish: prefiks + uzunlik + xabar"""
    m = xabar.encode("utf-8")
    return kek(b"\x19Ethereum Signed Message:\n" + str(len(m)).encode() + m)

def manzil(vk):
    return "0x" + kek(vk.to_string())[-20:].hex()

yopiq = 0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318
sk = SigningKey.from_secret_exponent(yopiq, curve=SECP256k1)
vk = sk.get_verifying_key()

xabar = "Men UniChain a'zosiman"
z = eip191(xabar)
rs = sk.sign_digest(z, sigencode=sigencode_string)

# Ethereum "past s" qoidasi (EIP-2): s > n/2 bo'lsa, n - s olinadi
n = SECP256k1.order
r, s_ = int.from_bytes(rs[:32], "big"), int.from_bytes(rs[32:], "big")
if s_ > n // 2:
    s_ = n - s_
rs = r.to_bytes(32, "big") + s_.to_bytes(32, "big")

# v qiymatini topish: qaysi ochiq kalit tiklansa, shu bizniki
for v in (27, 28):
    nomzodlar = VerifyingKey.from_public_key_recovery_with_digest(
        rs, z, SECP256k1, sigdecode=sigdecode_string)
    if nomzodlar[v - 27].to_string() == vk.to_string():
        break
imzo = "0x" + rs.hex() + format(v, "02x")

print("Manzil  :", manzil(vk))
print("Xabar   :", xabar)
print("Imzo    :", imzo)

# Tekshiruv 1: to'g'ri xabar
print("\nTo'g'ri xabar tekshiruvi   :", vk.verify_digest(rs, z, sigdecode=sigdecode_string))

# Tekshiruv 2: bitta belgi o'zgargan xabar
try:
    vk.verify_digest(rs, eip191(xabar + "!"), sigdecode=sigdecode_string)
    print("O'zgartirilgan xabar       : True")
except BadSignatureError:
    print("O'zgartirilgan xabar       : False  (imzo rad etildi)")

# Tekshiruv 3: imzodan manzilni tiklash (blokcheyn aynan shunday qiladi)
tiklangan = VerifyingKey.from_public_key_recovery_with_digest(
    rs, z, SECP256k1, sigdecode=sigdecode_string)[v - 27]
print("Imzodan tiklangan manzil   :", manzil(tiklangan))
