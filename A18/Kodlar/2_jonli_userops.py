# A18 · 2-skript: Sepolia'dagi haqiqiy ERC-4337 faolligi — EntryPoint v0.7 ning UserOperationEvent loglari
# Faqat o'qish. Ishga tushirish: python 2_jonli_userops.py [bloklar_soni=500]
import sys, collections
from web3 import Web3
from userop import ENTRYPOINT_V07

N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com", request_kwargs={"timeout": 30}))
MAVZU = Web3.keccak(text="UserOperationEvent(bytes32,address,address,uint256,bool,uint256,uint256)")
oxirgi = w3.eth.block_number
loglar = w3.eth.get_logs({"address": ENTRYPOINT_V07, "topics": [MAVZU], "fromBlock": oxirgi - N, "toBlock": oxirgi})

ops = []
for l in loglar:
    d = bytes(l["data"])                     # indexed bo'lmagan maydonlar: nonce, success, actualGasCost, actualGasUsed
    ops.append({"tx": l["transactionHash"].hex(), "sender": "0x" + l["topics"][2].hex()[-40:],
                "paymaster": "0x" + l["topics"][3].hex()[-40:], "success": int.from_bytes(d[32:64], "big") == 1,
                "cost": int.from_bytes(d[64:96], "big"), "gas": int.from_bytes(d[96:128], "big")})
if not ops:
    sys.exit(f"So'nggi {N} blokda UserOp topilmadi — bloklar sonini oshiring.")

txlar = collections.Counter(o["tx"] for o in ops)
homiyli = [o for o in ops if int(o["paymaster"], 16) != 0]
print(f"So'nggi {N} blok (#{oxirgi - N}…#{oxirgi}), EntryPoint v0.7 = {ENTRYPOINT_V07}")
print(f"  UserOp soni                  : {len(ops)}")
print(f"  handleOps tranzaksiyalari     : {len(txlar)}  (1 tranzaksiyada o'rtacha {len(ops) / len(txlar):.2f} UserOp)")
print(f"  Turli smart-akkauntlar        : {len({o['sender'] for o in ops})}")
print(f"  Paymaster to'lagan (homiyli)  : {len(homiyli)} ({len(homiyli) / len(ops):.0%})")
print(f"  Muvaffaqiyatli                : {sum(o['success'] for o in ops) / len(ops):.0%}")
print(f"  O'rtacha actualGasUsed        : {sum(o['gas'] for o in ops) / len(ops):,.0f}")
print(f"  Eng faol paymaster'lar        : {collections.Counter(o['paymaster'] for o in homiyli).most_common(3)}")
print(f"\nNamuna: blockscout yoki etherscan'da oching → tx 0x{ops[-1]['tx']}")
