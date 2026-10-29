# A6 · 1-skript: EIP-1559 tranzaksiyasi ichida nima bor? (oflayn, tarmoqqa yuborilmaydi)
# O'rnatish: pip install eth-account
from eth_account import Account

# Hardhat/Foundry'ning hammaga ma'lum TEST kaliti (A5 dagi test iborasining 0-hisobi).
# Unga hech qachon real mablag' yubormang!
TEST_KALIT = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
GWEI = 10**9

def tx_tuz(nonce, tip_gwei=1.5, max_gwei=30, qiymat_eth=0.01, kimga="0x70997970C51812dc3A010C7d01b50e0d17dc79C8"):
    return {"type": 2, "chainId": 11155111,                 # Sepolia
            "nonce": nonce, "to": kimga, "value": int(qiymat_eth * 10**18),
            "gas": 21000,                                   # oddiy ETH o'tkazmasi
            "maxPriorityFeePerGas": int(tip_gwei * GWEI),   # validatorga choy puli
            "maxFeePerGas": int(max_gwei * GWEI)}           # to'lashga tayyor bo'lgan eng yuqori narx

if __name__ == "__main__":
    hisob = Account.from_key(TEST_KALIT)
    print("Yuboruvchi:", hisob.address)
    tx = tx_tuz(nonce=0)
    for k, v in tx.items(): print(f"  {k:22} = {v}")
    imz = hisob.sign_transaction(tx)
    raw = imz.raw_transaction.hex()
    print("\nXom tranzaksiya:", raw[:66] + "…", f"({len(raw)//2} bayt)")
    print("Birinchi bayt 02 → EIP-1559 turi:", raw[:2] == "02")
    print("Tx hash        :", imz.hash.hex())
    print("Imzodan tiklangan yuboruvchi:", Account.recover_transaction(imz.raw_transaction))
    print("\nFaqat nonce'ni 1 ga o'zgartirsak:")
    print("Tx hash        :", hisob.sign_transaction(tx_tuz(nonce=1)).hash.hex())
    print("\nBoshqa tarmoq (chainId=84532, Base Sepolia) uchun xuddi shu tx:")
    t2 = tx_tuz(nonce=0); t2["chainId"] = 84532
    print("Tx hash        :", hisob.sign_transaction(t2).hash.hex())
