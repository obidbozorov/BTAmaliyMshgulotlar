# A9 · 1-skript: 2/3 multisig modeli — tranzaksiya faqat yetarli imzo yig'ilganda bajariladi
# O'rnatish: pip install eth-account
# Hardhat'ning hammaga ma'lum TEST kalitlari (#0, #1, #2). Real mablag' uchun ishlatmang!
from eth_account import Account
from eth_account.messages import encode_defunct
from Crypto.Hash import keccak

KALITLAR = ["0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
            "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",
            "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"]

class Multisig:
    def __init__(self, egalar, chegara):
        self.egalar = {a.lower() for a in egalar}; self.chegara = chegara; self.nonce = 0
    def tx_xeshi(self, kimga, qiymat):
        h = keccak.new(digest_bits=256)
        h.update(f"{kimga.lower()}|{qiymat}|{self.nonce}".encode())          # nonce — qayta ishlatishdan himoya
        return h.digest()
    def bajar(self, kimga, qiymat, imzolar):
        x = encode_defunct(self.tx_xeshi(kimga, qiymat))
        imzolovchilar = {Account.recover_message(x, signature=s).lower() for s in imzolar}
        haqiqiy = imzolovchilar & self.egalar
        begona = imzolovchilar - self.egalar
        if len(haqiqiy) < self.chegara:
            return f"RAD: ega imzolari {len(haqiqiy)} ta, kerak {self.chegara} ta" + (f" (tanilmagan imzo: {len(begona)})" if begona else "")
        self.nonce += 1
        return f"BAJARILDI: ega imzolari {len(haqiqiy)} ta (chegara {self.chegara}), yangi nonce = {self.nonce}"

if __name__ == "__main__":
    egalar = [Account.from_key(k) for k in KALITLAR]
    for i, e in enumerate(egalar): print(f"Ega {i+1}: {e.address}")
    safe = Multisig([e.address for e in egalar], chegara=2)
    kimga, qiymat = "0x90F79bf6EB2c4f870365E785982E1f101E93b906", 10**17
    imzola = lambda e: e.sign_message(encode_defunct(safe.tx_xeshi(kimga, qiymat))).signature
    print("\n1) Faqat Ega 1 imzoladi   →", safe.bajar(kimga, qiymat, [imzola(egalar[0])]))
    s1, s3 = imzola(egalar[0]), imzola(egalar[2])
    print("2) Ega 1 + Ega 3          →", safe.bajar(kimga, qiymat, [s1, s3]))
    print("3) Xuddi o'sha imzolar qayta →", safe.bajar(kimga, qiymat, [s1, s3]))
    begona = Account.create()
    print("4) Ega 2 + begona kalit   →", safe.bajar(kimga, qiymat, [imzola(egalar[1]), imzola(begona)]))
