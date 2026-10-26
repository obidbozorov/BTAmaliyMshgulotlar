# 1-topshiriq: Kalit juftligi va manzillar (Ethereum + Bitcoin)
# Kerak: pip install ecdsa pycryptodome
import secrets
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak, SHA256, RIPEMD160

ALIFBO = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def base58(b):
    son = int.from_bytes(b, "big"); s = ""
    while son: son, q = divmod(son, 58); s = ALIFBO[q] + s
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + s

def eth_manzil(pub64):
    h = keccak.new(digest_bits=256); h.update(pub64)
    return "0x" + h.digest()[-20:].hex()

def btc_manzil(pub_siqiq):
    h160 = RIPEMD160.new(SHA256.new(pub_siqiq).digest()).digest()
    v = b"\x00" + h160
    return base58(v + SHA256.new(SHA256.new(v).digest()).digest()[:4])

# Namuna uchun ma'lum kalit; o'zingiznikini yaratish uchun keyingi satrni oching
yopiq = 0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318
# yopiq = secrets.randbelow(SECP256k1.order - 1) + 1

sk  = SigningKey.from_secret_exponent(yopiq, curve=SECP256k1)
pub = sk.get_verifying_key()

print("Yopiq kalit :", format(yopiq, "064x"))
print("Ochiq kalit :", pub.to_string().hex())
print("Siqiq kalit :", pub.to_string("compressed").hex())
print("Ethereum    :", eth_manzil(pub.to_string()))
print("Bitcoin     :", btc_manzil(pub.to_string("compressed")))
