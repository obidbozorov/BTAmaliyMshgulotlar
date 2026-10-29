# A15 · 3-skript: joriy narxlarni tarmoqdan o'qiydi va modelni Base'ning GasPriceOracle kontrakti bilan solishtiradi
# Faqat o'qish (eth_call) — hamyon, kalit va test ETH kerak emas. Ishga tushirish: python 3_jonli_tekshir.py [--testnet]
import json, sys
from web3 import Web3
from l2_formula import l1_data_fee
import importlib; model = importlib.import_module("2_komissiya_modeli")

TESTNET = "--testnet" in sys.argv
L1_RPC = "https://ethereum-sepolia-rpc.publicnode.com" if TESTNET else "https://ethereum-rpc.publicnode.com"
L2_RPC = "https://sepolia.base.org" if TESTNET else "https://mainnet.base.org"
ORACLE = "0x420000000000000000000000000000000000000F"          # OP Stack'dagi oldindan joylangan kontrakt
ABI = [{"name": n, "type": "function", "stateMutability": "view", "inputs": [], "outputs": [{"type": "uint256"}]}
       for n in ("l1BaseFee", "blobBaseFee", "baseFeeScalar", "blobBaseFeeScalar")] + \
      [{"name": "getL1Fee", "type": "function", "stateMutability": "view", "inputs": [{"type": "bytes"}], "outputs": [{"type": "uint256"}]}]

def ulan(url):
    w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 20}))
    w3.eth.block_number                                     # ulanishni tekshirish
    return w3

try:
    l1, l2 = ulan(L1_RPC), ulan(L2_RPC)
except Exception as e:
    sys.exit(f"RPC'ga ulanib bo'lmadi ({type(e).__name__}). Internetni tekshiring yoki 2_komissiya_modeli.py dan foydalaning.")

b1, b2 = l1.eth.get_block("latest"), l2.eth.get_block("latest")
oracle = l2.eth.contract(address=ORACLE, abi=ABI)
p = {n: oracle.functions[n]().call(block_identifier=b2.number) for n in ("l1BaseFee", "blobBaseFee", "baseFeeScalar", "blobBaseFeeScalar")}
tip1 = l1.eth.max_priority_fee
tip2 = l2.eth.max_priority_fee
print(f"{'Testnet' if TESTNET else 'Mainnet'}: L1 blok #{b1.number}, baseFee = {b1.baseFeePerGas / 1e9:.4f} gwei, tip = {tip1 / 1e9:.4f} gwei")
print(f"         L2 blok #{b2.number}, baseFee = {b2.baseFeePerGas / 1e9:.4f} gwei, tip = {tip2 / 1e9:.4f} gwei")
print(f"GasPriceOracle: {p}")

with open("olchov.json", encoding="utf-8") as f:
    olchov = json.load(f)
print("\nModel va kontrakt (getL1Fee) natijasi:")
for o in olchov:
    tx = bytes.fromhex(o["tx_hex"])
    zanjir = oracle.functions.getL1Fee(tx).call(block_identifier=b2.number)
    biz = l1_data_fee(tx, p["l1BaseFee"], p["blobBaseFee"], p["baseFeeScalar"], p["blobBaseFeeScalar"])
    print(f"  {o['amal']:26} kontrakt {zanjir:>14,} wei · model {biz:>14,} wei · mos: {zanjir == biz}")

eth = {"base_fee": b1.baseFeePerGas, "tip": tip1}
base = {"l2_base_fee": b2.baseFeePerGas, "l2_tip": tip2, "l1_base_fee": p["l1BaseFee"], "blob_base_fee": p["blobBaseFee"],
        "base_fee_scalar": p["baseFeeScalar"], "blob_base_fee_scalar": p["blobBaseFeeScalar"]}
model.jadval(model.hisobla(olchov, eth, base), "Joriy narxlar bilan")
