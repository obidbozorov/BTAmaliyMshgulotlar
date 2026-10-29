# A8 · 1-skript: explorer ko'rsatadigan maydonlarni xom tranzaksiyadan o'zimiz ajratamiz
# O'rnatish: pip install eth-account   (rlp kutubxonasi u bilan birga o'rnatiladi)
import rlp
from eth_account import Account
from Crypto.Hash import keccak

# A7 dagi 1_tranzaksiya.py chiqargan xom tranzaksiya (test kaliti, Sepolia, nonce 0)

def toliq_xom():
    tx = {"type": 2, "chainId": 11155111, "nonce": 0, "to": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
          "value": 10**16, "gas": 21000, "maxPriorityFeePerGas": 1_500_000_000, "maxFeePerGas": 30_000_000_000}
    return Account.from_key("0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80").sign_transaction(tx).raw_transaction

if __name__ == "__main__":
    raw = bytes(toliq_xom())
    print("Tur bayti:", hex(raw[0]), "→ EIP-1559")
    f = rlp.decode(raw[1:])
    nomlar = ["chainId", "nonce", "maxPriorityFeePerGas", "maxFeePerGas", "gas", "to", "value", "data", "accessList", "yParity", "r", "s"]
    for n, v in zip(nomlar, f):
        if isinstance(v, list): print(f"  {n:22} {v}")
        elif n in ("to", "data", "r", "s"): print(f"  {n:22} 0x{v.hex()}")
        else: print(f"  {n:22} {int.from_bytes(v, 'big') if v else 0}")
    h = keccak.new(digest_bits=256); h.update(raw)
    print("\nTx hash = keccak256(xom) =", "0x" + h.hexdigest())
    print("From (imzodan)          =", Account.recover_transaction(raw))
