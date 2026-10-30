# A21 · 1-skript: a'zolar ro'yxatidan Merkle root va har bir a'zoning proof'ini tayyorlaydi
# Ishga tushirish: python 1_royxat.py [azolar.txt]  →  dao_proofs.json (Remix'ga nusxalash uchun)
import json, sys
from merkle import barg, daraxt_qur, proof_ol, royxatni_oqi

azolar = royxatni_oqi(sys.argv[1] if len(sys.argv) > 1 else "azolar.txt")
d = daraxt_qur([barg(m) for m in azolar])
root = "0x" + d[-1][0].hex()
print(f"A'zolar: {len(azolar)} · daraxt balandligi: {len(d) - 1}")
print(f"MERKLE ROOT: {root}   ← DAO konstruktoriga shuni bering (A3 dagi root bilan solishtiring)\n")
natija = {"root": root, "azolar": {}}
for i, m in enumerate(azolar):
    p = ["0x" + x.hex() for x in proof_ol(d, i)]
    natija["azolar"][m] = p
    print(f"{i}. {m}\n   proof (Remix formatida): {json.dumps(p)}")
with open("dao_proofs.json", "w", encoding="utf-8") as f:
    json.dump(natija, f, indent=2)
print("\nSaqlandi: dao_proofs.json")
