# A21 · A3 dagi Merkle daraxti funksiyalari (3_merkle_royxat.py bilan aynan bir xil formula)
from Crypto.Hash import keccak

def kek(b):
    h = keccak.new(digest_bits=256); h.update(b); return h.digest()

def barg(manzil):
    """Solidity: keccak256(bytes.concat(keccak256(abi.encode(addr))))"""
    return kek(kek(bytes(12) + bytes.fromhex(manzil[2:].lower())))

def juft(a, b):
    return kek(a + b) if a < b else kek(b + a)          # OpenZeppelin tartiblangan juftlik

def daraxt_qur(barglar):
    darajalar = [barglar]
    while len(darajalar[-1]) > 1:
        j = darajalar[-1]
        darajalar.append([juft(j[i], j[i + 1]) if i + 1 < len(j) else j[i] for i in range(0, len(j), 2)])
    return darajalar

def proof_ol(darajalar, indeks):
    proof = []
    for d in darajalar[:-1]:
        if indeks ^ 1 < len(d):
            proof.append(d[indeks ^ 1])
        indeks //= 2
    return proof

def royxatni_oqi(fayl="azolar.txt"):
    with open(fayl, encoding="utf-8") as f:
        return [q.strip() for q in f if q.strip() and not q.startswith("#")]
