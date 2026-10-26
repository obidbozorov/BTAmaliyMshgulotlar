# 1-topshiriq: Bitcoin blok xeshini qo'lda hisoblash
# Genesis blok (Blok #0) maydonlari — mempool.space dan olingan
import hashlib, struct

version     = 1
oldingi     = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
vaqt        = 1231006505
bits        = 0x1d00ffff
nonce       = 2083236893

# Header 80 bayt qilib yig'iladi (barcha sonlar little-endian tartibda)
header  = struct.pack("<I", version)
header += bytes.fromhex(oldingi)[::-1]
header += bytes.fromhex(merkle_root)[::-1]
header += struct.pack("<I", vaqt)
header += struct.pack("<I", bits)
header += struct.pack("<I", nonce)

print("Header uzunligi :", len(header), "bayt")

# Bitcoin ikki marta SHA-256 ishlatadi
xesh = hashlib.sha256(hashlib.sha256(header).digest()).digest()
blok_xeshi = xesh[::-1].hex()

print("Hisoblangan xesh:", blok_xeshi)
print("Kutilgan xesh   : 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
print("Mos keldimi     :", blok_xeshi == "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
