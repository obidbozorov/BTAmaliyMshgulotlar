# A15 · 4-skript: o'zingiz yuborgan tranzaksiyaning komissiyasini qismlarga ajratadi
# Ishga tushirish: python 4_kvitansiya.py <tx_hash> [sepolia | base-sepolia]   (standart: base-sepolia)
import sys
from web3 import Web3

RPC = {"sepolia": "https://ethereum-sepolia-rpc.publicnode.com", "base-sepolia": "https://sepolia.base.org"}
if len(sys.argv) < 2:
    sys.exit("Foydalanish: python 4_kvitansiya.py 0x<tx_hash> [sepolia | base-sepolia]")
tarmoq = sys.argv[2] if len(sys.argv) > 2 else "base-sepolia"
w3 = Web3(Web3.HTTPProvider(RPC[tarmoq], request_kwargs={"timeout": 20}))
r = w3.eth.get_transaction_receipt(sys.argv[1])
blok = w3.eth.get_block(r.blockNumber)

ijro = r.gasUsed * r.effectiveGasPrice
yoqildi = r.gasUsed * blok.baseFeePerGas
print(f"Tarmoq: {tarmoq} · blok #{r.blockNumber} · holat: {'muvaffaqiyatli' if r.status else 'XATO'}")
print(f"gasUsed            : {r.gasUsed:,}")
print(f"effectiveGasPrice  : {r.effectiveGasPrice / 1e9:.6f} gwei  (baseFee {blok.baseFeePerGas / 1e9:.6f} + tip)")
l1_fee = int(r.get("l1Fee", "0x0"), 16) if isinstance(r.get("l1Fee"), str) else r.get("l1Fee", 0)
# Ethereum'da baseFee qismi yoqiladi (EIP-1559); OP Stack'da esa u yoqilmaydi, BaseFeeVault kontraktiga tushadi
qism = "BaseFeeVault'ga" if l1_fee else "yoqildi"
print(f"Ijro komissiyasi   : {ijro / 1e18:.12f} ETH  ({qism}: {yoqildi / 1e18:.12f}, tip: {(ijro - yoqildi) / 1e18:.12f})")
if l1_fee:                                                   # faqat OP Stack (Base, Optimism) kvitansiyasida bo'ladi
    print(f"L1 ma'lumot (l1Fee): {l1_fee / 1e18:.12f} ETH")
    for k in ("l1GasUsed", "l1GasPrice", "l1BlobBaseFee", "l1BaseFeeScalar", "l1BlobBaseFeeScalar"):
        if k in r: print(f"   {k:18}: {int(r[k], 16) if isinstance(r[k], str) else r[k]:,}")
print(f"JAMI               : {(ijro + l1_fee) / 1e18:.12f} ETH  — explorer'dagi “Transaction Fee” bilan solishtiring")
