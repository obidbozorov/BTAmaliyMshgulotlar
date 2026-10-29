# A5 · 2-skript: bitta iboradan cheksiz manzil — HD-hamyon (BIP-32/44)
# MetaMask yo'li: m/44'/60'/0'/0/i  (44 — BIP-44, 60 — Ethereum, i — hisob raqami)
# O'rnatish: pip install ecdsa pycryptodome
import hashlib, hmac, unicodedata
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak

N = SECP256k1.order

def ibora_seed(ibora: str, parol: str = "") -> bytes:      # BIP-39: PBKDF2, 2048 marta
    m = unicodedata.normalize("NFKD", ibora).encode()
    s = unicodedata.normalize("NFKD", "mnemonic" + parol).encode()
    return hashlib.pbkdf2_hmac("sha512", m, s, 2048)

def siqilgan_ochiq(k: int) -> bytes:
    return SigningKey.from_secret_exponent(k, curve=SECP256k1).get_verifying_key().to_string("compressed")

def bola(k: int, zanjir: bytes, i: int):                    # BIP-32 bola kalit
    if i >= 0x80000000:  data = b"\x00" + k.to_bytes(32, "big") + i.to_bytes(4, "big")   # qattiq (')
    else:                data = siqilgan_ochiq(k) + i.to_bytes(4, "big")
    I = hmac.new(zanjir, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % N, I[32:]

def yol_boyicha(seed: bytes, yol: str) -> int:
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], "big"), I[32:]
    for q in yol.split("/")[1:]:
        k, c = bola(k, c, int(q.rstrip("'")) + (0x80000000 if q.endswith("'") else 0))
    return k

def eip55(manzil_hex: str) -> str:
    h = keccak.new(digest_bits=256); h.update(manzil_hex.encode()); hx = h.hexdigest()
    return "0x" + "".join(c.upper() if int(hx[i], 16) >= 8 else c for i, c in enumerate(manzil_hex))

def eth_manzil(k: int) -> str:
    pub = SigningKey.from_secret_exponent(k, curve=SECP256k1).get_verifying_key().to_string()
    h = keccak.new(digest_bits=256); h.update(pub)
    return eip55(h.digest()[-20:].hex())

if __name__ == "__main__":
    # Hardhat/Foundry'ning hammaga ma'lum TEST iborasi — unda hech qachon real pul saqlamang!
    IBORA = "test test test test test test test test test test test junk"
    seed = ibora_seed(IBORA)
    print("Seed (64 bayt):", seed.hex()[:32] + "…")
    for i in range(3):
        print(f"m/44'/60'/0'/0/{i} →", eth_manzil(yol_boyicha(seed, f"m/44'/60'/0'/0/{i}")))
    print("\nXuddi shu ibora + parol (25-so'z) 'PROFI':")
    print("m/44'/60'/0'/0/0 →", eth_manzil(yol_boyicha(ibora_seed(IBORA, "PROFI"), "m/44'/60'/0'/0/0")))
