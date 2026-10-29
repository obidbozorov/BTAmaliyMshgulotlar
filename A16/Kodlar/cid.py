# A16 · IPFS CID (v1, raw, sha2-256) — fayl mazmunidan manzil hisoblash
# Bitta blokga sig'adigan (≤ 256 KiB) fayl uchun `ipfs add --cid-version=1 --raw-leaves` aynan shu CID ni beradi.
import hashlib, base64

def cid_v1(mazmun: bytes) -> str:
    multihash = bytes([0x12, 0x20]) + hashlib.sha256(mazmun).digest()   # 0x12 = sha2-256, 0x20 = 32 bayt
    cid = bytes([0x01, 0x55]) + multihash                               # 0x01 = CIDv1, 0x55 = raw kodek
    return "b" + base64.b32encode(cid).decode().lower().rstrip("=")    # "b" = base32 multibase prefiksi

def cid_dan_xesh(cid: str) -> bytes:
    """bafkrei… ko'rinishidagi CID dan sha256 xeshni ajratib oladi"""
    assert cid.startswith("b"), "Faqat base32 (b…) CIDv1 qo'llanadi"
    s = cid[1:].upper(); s += "=" * (-len(s) % 8)
    b = base64.b32decode(s)
    assert b[:4] == bytes([0x01, 0x55, 0x12, 0x20]), "Bu CIDv1 raw sha2-256 emas (masalan, papka yoki Qm… CIDv0)"
    return b[4:]
