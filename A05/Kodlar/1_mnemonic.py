# A5 · 1-skript: BIP-39 — 12 so'zli tiklash iborasi (seed phrase) qanday yasaladi
# O'rnatish: pip install mnemonic pycryptodome
# DIQQAT: bu yerda yaratilgan iboralar faqat o'quv uchun. Real hamyonda ishlatmang!
import hashlib, secrets, os
import mnemonic

ROYXAT = open(os.path.join(os.path.dirname(mnemonic.__file__), "wordlist", "english.txt")).read().split()
assert len(ROYXAT) == 2048          # 2048 = 2^11 → har bir so'z 11 bit

def entropiyadan_ibora(entropiya: bytes) -> str:
    bitlar = len(entropiya) * 8                       # 128 bit
    cs_uzunlik = bitlar // 32                         # nazorat summasi: 4 bit
    cs = hashlib.sha256(entropiya).digest()
    hammasi = bin(int.from_bytes(entropiya, "big"))[2:].zfill(bitlar) + \
              bin(int.from_bytes(cs, "big"))[2:].zfill(256)[:cs_uzunlik]
    return " ".join(ROYXAT[int(hammasi[i:i+11], 2)] for i in range(0, len(hammasi), 11))

def ibora_togrimi(ibora: str) -> bool:
    sozlar = ibora.split()
    if any(s not in ROYXAT for s in sozlar): return False
    bitlar = "".join(bin(ROYXAT.index(s))[2:].zfill(11) for s in sozlar)
    ent_bit = len(bitlar) * 32 // 33
    entropiya = int(bitlar[:ent_bit], 2).to_bytes(ent_bit // 8, "big")
    cs = bin(int.from_bytes(hashlib.sha256(entropiya).digest(), "big"))[2:].zfill(256)[:len(bitlar) - ent_bit]
    return bitlar[ent_bit:] == cs

if __name__ == "__main__":
    # 1) Namuna: hamma bitlari 0 bo'lgan entropiya (BIP-39 rasmiy test vektori)
    namuna = entropiyadan_ibora(bytes(16))
    print("Nol entropiya    :", namuna)
    # 2) Haqiqiy tasodifiy entropiya
    ent = secrets.token_bytes(16)
    ibora = entropiyadan_ibora(ent)
    print("Entropiya (hex)  :", ent.hex())
    print("Sizning iborangiz:", ibora)
    print("Kutubxona bilan mos:", ibora == mnemonic.Mnemonic("english").to_mnemonic(ent))
    # 3) Nazorat summasi: bitta so'zni almashtiramiz
    sozlar = ibora.split(); sozlar[5] = "apple" if sozlar[5] != "apple" else "zoo"
    print("To'g'ri ibora     :", ibora_togrimi(ibora))
    print("6-so'z almashgan  :", ibora_togrimi(" ".join(sozlar)))
    # 4) Kuch bilan topish (brute force) qancha vaqt oladi?
    variant = 2 ** 128
    sekund = variant / 1e12                 # sekundiga 1 trillion urinish
    print(f"Variantlar soni  : 2^128 ≈ {variant:.2e}")
    print(f"1 trln/s tezlikda: ≈ {sekund/3.156e7:.2e} yil")
