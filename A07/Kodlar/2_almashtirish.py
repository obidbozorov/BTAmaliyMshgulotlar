# A6 · 2-skript: tezlashtirish (speed-up) va bekor qilish (cancel) qanday ishlaydi?
# Ikkalasi ham — xuddi shu nonce bilan, yuqoriroq komissiyali YANGI tranzaksiya.
# O'rnatish: pip install eth-account
from eth_account import Account
TEST_KALIT = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
GWEI = 10**9
OSHIRISH = 1.10        # Geth qoidasi: almashtiruvchi tx komissiyasi kamida 10% yuqori bo'lishi shart

def almashtirish_narxi(eski_tip, eski_max, koef=OSHIRISH):
    return int(eski_tip * koef) + 1, int(eski_max * koef) + 1

if __name__ == "__main__":
    h = Account.from_key(TEST_KALIT)
    asl = {"type": 2, "chainId": 11155111, "nonce": 7, "to": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
           "value": 10**16, "gas": 21000, "maxPriorityFeePerGas": 1 * GWEI, "maxFeePerGas": 2 * GWEI}
    tip, mx = almashtirish_narxi(asl["maxPriorityFeePerGas"], asl["maxFeePerGas"])
    tez = {**asl, "maxPriorityFeePerGas": tip, "maxFeePerGas": mx}
    bekor = {**asl, "to": h.address, "value": 0, "maxPriorityFeePerGas": tip, "maxFeePerGas": mx}
    for nom, t in [("Asl tranzaksiya", asl), ("Tezlashtirish ", tez), ("Bekor qilish  ", bekor)]:
        print(f"{nom}: nonce={t['nonce']}  kimga={t['to'][:10]}…  qiymat={t['value']/1e18} ETH  "
              f"tip={t['maxPriorityFeePerGas']/GWEI:.4f} gwei  max={t['maxFeePerGas']/GWEI:.4f} gwei")
        print("   hash:", h.sign_transaction(t).hash.hex())
    print("\nUchchalasining nonce'i bir xil → blokka faqat BITTASI tushadi.")
    kam = {**asl, "maxPriorityFeePerGas": int(1.05 * GWEI), "maxFeePerGas": int(2.1 * GWEI)}
    ok = kam["maxPriorityFeePerGas"] >= tip and kam["maxFeePerGas"] >= mx
    print("Faqat 5% oshirilgan almashtirish qabul qilinadimi?", ok, "→ 'replacement transaction underpriced'")
