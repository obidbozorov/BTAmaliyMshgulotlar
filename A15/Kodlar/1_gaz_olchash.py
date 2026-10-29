# A15 · 1-skript: amallarning gaz sarfini mahalliy EVM'da o'lchaydi va olchov.json ga yozadi
# O'rnatish: pip install -r requirements.txt   ·   Ishga tushirish: python 1_gaz_olchash.py
import json, solcx
from web3 import Web3, EthereumTesterProvider
from l2_formula import imzosiz_1559

solcx.install_solc("0.8.28")
k = solcx.compile_files(["Token.sol"], output_values=["abi", "bin"], solc_version="0.8.28")["Token.sol:Token"]
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18

def calldata_gaz(data: bytes) -> int:
    """EIP-2028: har bir nol bayt 4 gaz, nol bo'lmagan bayt 16 gaz"""
    return sum(4 if x == 0 else 16 for x in data)

olchov = []
def yoz(nom, tx_hash, kimga, data: bytes, qiymat=0):
    r = w3.eth.wait_for_transaction_receipt(tx_hash)
    # Base (chainId 8453) uchun xuddi shu tranzaksiyaning imzosiz baytlari — L1 ma'lumot komissiyasi shundan hisoblanadi
    raw = imzosiz_1559(8453, 7, 10**6, 10**7, r.gasUsed, kimga, qiymat, data)
    olchov.append({"amal": nom, "gaz": r.gasUsed, "calldata_bayt": len(data),
                   "calldata_gaz": calldata_gaz(data), "tx_bayt": len(raw), "tx_hex": raw.hex()})

# 1) Oddiy ETH o'tkazmasi
yoz("ETH o'tkazma", w3.eth.send_transaction({"from": A[0], "to": A[1], "value": E}), A[1], b"", E)
# 2) Token deploy
dep = w3.eth.contract(abi=k["abi"], bytecode=k["bin"]).constructor(1000)
h = dep.transact({"from": A[0]})
yoz("Token deploy", h, None, bytes.fromhex(dep.data_in_transaction[2:]))
t = w3.eth.contract(address=w3.eth.get_transaction_receipt(h).contractAddress, abi=k["abi"])

def chaqir(nom, fn, frm=0):
    data = bytes.fromhex(fn.build_transaction({"from": A[frm], "gas": 10**6})["data"][2:])
    yoz(nom, fn.transact({"from": A[frm]}), t.address, data)

chaqir("transfer (yangi oluvchi)", t.functions.transfer(A[1], 25 * E))
chaqir("transfer (bor oluvchi)", t.functions.transfer(A[1], 5 * E))
chaqir("approve", t.functions.approve(A[2], 10 * E), 1)
chaqir("transferFrom", t.functions.transferFrom(A[1], A[3], 4 * E), 2)

print(f"{'Amal':26}{'Gaz':>10}{'Calldata, B':>13}{'Calldata gazi':>15}{'Ulushi':>9}")
for o in olchov:
    print(f"{o['amal']:26}{o['gaz']:>10,}{o['calldata_bayt']:>13,}{o['calldata_gaz']:>15,}{o['calldata_gaz'] / o['gaz']:>9.1%}")
with open("olchov.json", "w", encoding="utf-8") as f:
    json.dump(olchov, f, ensure_ascii=False, indent=1)
print("\nSaqlandi: olchov.json  (2_komissiya_modeli.py va 3_jonli_tekshir.py uchun)")
