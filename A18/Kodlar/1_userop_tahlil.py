# A18 · 1-skript: UserOperation qadamma-qadam — maydonlar, xesh, imzo, maksimal xarajat
# Oxirida xeshni Sepolia'dagi haqiqiy EntryPoint v0.7 bilan solishtiradi (internet bo'lmasa, o'tkazib yuboriladi)
# Ishga tushirish: python 1_userop_tahlil.py
from eth_account import Account
from eth_account.messages import encode_defunct
from userop import UserOp, userop_hash, imzola, execute_calldata, ENTRYPOINT_V07

EGA = Account.from_key("0x" + "4a" * 32)                         # o'quv kaliti — real mablag' uchun emas!
AKKAUNT = "0x" + "c0de" * 10                                      # smart-akkaunt manzili (namuna)
ALI = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
SEPOLIA = 11155111

op = UserOp(sender=AKKAUNT, nonce=0, callData=execute_calldata(ALI, 10**16))
print("1) UserOperation maydonlari")
for k, v in vars(op).items():
    print(f"   {k:22} {('0x' + v.hex()) if isinstance(v, bytes) else v}")
print(f"   accountGasLimits (qadoqlangan) 0x{op.accountGasLimits().hex()}")
print(f"   gasFees          (qadoqlangan) 0x{op.gasFees().hex()}")

maks = (op.verificationGasLimit + op.callGasLimit + op.preVerificationGas) * op.maxFeePerGas
print(f"\n2) Eng ko'p xarajat (prefund) = (150 000 + 100 000 + 50 000) × 2 gwei = {maks / 1e18:.4f} ETH")

h = userop_hash(op, ENTRYPOINT_V07, SEPOLIA)
print(f"\n3) userOpHash (Sepolia, EntryPoint v0.7) = 0x{h.hex()}")
print(f"   Boshqa tarmoqda (Base Sepolia 84532)  = 0x{userop_hash(op, ENTRYPOINT_V07, 84532).hex()}")

imzola(op, EGA.key, ENTRYPOINT_V07, SEPOLIA)
print(f"\n4) Egasining imzosi ({len(op.signature)} bayt) = 0x{op.signature.hex()[:40]}…")
print(f"   Imzodan tiklangan manzil: {Account.recover_message(encode_defunct(h), signature=op.signature)}  (egasi: {EGA.address})")

try:
    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com", request_kwargs={"timeout": 15}))
    abi = [{"name": "getUserOpHash", "type": "function", "stateMutability": "view", "outputs": [{"type": "bytes32"}],
            "inputs": [{"name": "op", "type": "tuple", "components": [{"name": n, "type": t} for n, t in [
                ("sender", "address"), ("nonce", "uint256"), ("initCode", "bytes"), ("callData", "bytes"), ("accountGasLimits", "bytes32"),
                ("preVerificationGas", "uint256"), ("gasFees", "bytes32"), ("paymasterAndData", "bytes"), ("signature", "bytes")]]}]}]
    z = w3.eth.contract(address=ENTRYPOINT_V07, abi=abi).functions.getUserOpHash(op.kortej()).call()
    print(f"\n5) Sepolia EntryPoint.getUserOpHash = 0x{z.hex()} → mos: {z == h}")
except Exception as e:
    print(f"\n5) Sepolia bilan solishtirib bo'lmadi ({type(e).__name__}) — internetni tekshiring")
