# A8 · 3-skript: Bitcoin bloki xeshini o'zimiz hisoblaymiz va explorer bilan solishtiramiz
import hashlib, struct

def blok_xeshi(versiya, oldingi, merkle, vaqt, bits, nonce):
    sarlavha = (struct.pack("<I", versiya) + bytes.fromhex(oldingi)[::-1] + bytes.fromhex(merkle)[::-1]
                + struct.pack("<III", vaqt, bits, nonce))           # 80 bayt, little-endian
    assert len(sarlavha) == 80
    return hashlib.sha256(hashlib.sha256(sarlavha).digest()).digest()[::-1].hex()

def maqsad(bits):                                                  # “bits” → maqsad son
    eksp, mant = bits >> 24, bits & 0xFFFFFF
    return mant * 2 ** (8 * (eksp - 3))

if __name__ == "__main__":
    # Genezis bloki (0-blok), 2009-yil 3-yanvar — mempool.space/block/0 bilan solishtiring
    h = blok_xeshi(1, "00" * 32, "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
                   1231006505, 0x1d00ffff, 2083236893)
    print("Hisoblangan xesh:", h)
    print("Kutilgan        : 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
    print("Mos keldimi     :", h == "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
    T = maqsad(0x1d00ffff)
    print("Maqsad (target) : 0x" + format(T, "064x"))
    print("Xesh < maqsad   :", int(h, 16) < T)
    print("Boshidagi nol bitlar:", 256 - int(h, 16).bit_length())
    print("Nonce 1 ga o'zgarsa  :", blok_xeshi(1, "00"*32, "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b", 1231006505, 0x1d00ffff, 2083236894))
