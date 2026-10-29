# A18 · ERC-4337 oqimini mahalliy EVM'da sinovchi 12 ta tekshiruv
# Bundler (A[9]) → MiniEntryPoint.handleOps → MiniHisob.validateUserOp → execute;  gazni akkaunt yoki MiniHomiy to'laydi
# Ishga tushirish: python test_4337.py
import solcx
from web3 import Web3, EthereumTesterProvider
from web3.logs import DISCARD
from eth_account import Account
from userop import UserOp, imzola, userop_hash, execute_calldata, batch_calldata

solcx.install_solc("0.8.28")
B = {k.split(":")[1]: v for k, v in solcx.compile_files(["MiniEntryPoint.sol", "MiniHisob.sol", "MiniHomiy.sol", "Token.sol"],
     output_values=["abi", "bin"], solc_version="0.8.28").items()}
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18
BUNDLER, ALI = A[9], A[1]
EGA = Account.from_key("0x" + "4a" * 32)          # akkaunt egasining kaliti — bu EOA da ETH umuman yo'q!
YANGI_EGA = Account.from_key("0x" + "5b" * 32)
def dep(n, *a):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor(*a).transact({"from": A[0]}))
    return w3.eth.contract(address=r.contractAddress, abi=B[n]["abi"])
ep = dep("MiniEntryPoint"); hisob = dep("MiniHisob", ep.address, EGA.address)
homiy = dep("MiniHomiy", ep.address); token = dep("Token", 1000)
CHAIN = w3.eth.chain_id
w3.eth.send_transaction({"from": A[0], "to": hisob.address, "value": 2 * E})                       # akkauntga ETH
w3.eth.wait_for_transaction_receipt(token.functions.transfer(hisob.address, 100 * E).transact({"from": A[0]}))
w3.eth.wait_for_transaction_receipt(ep.functions.depositTo(homiy.address).transact({"from": A[0], "value": E}))

def op_tuz(calldata, kalit=EGA.key, key=0, **kw):
    op = UserOp(hisob.address, ep.functions.getNonce(hisob.address, key).call(), calldata, **kw)
    return imzola(op, kalit, ep.address, CHAIN)
def yubor(*ops):
    r = w3.eth.wait_for_transaction_receipt(ep.functions.handleOps([o.kortej() for o in ops], BUNDLER).transact({"from": BUNDLER}))
    return r, ep.events.UserOperationEvent().process_receipt(r, errors=DISCARD)   # Token loglari tashlab yuboriladi
def rad(ops, matn):
    try: ep.functions.handleOps([o.kortej() for o in ops], BUNDLER).call({"from": BUNDLER}); return False
    except Exception as e: return matn in str(e)
ball, natijalar = 0, []
def tek(nom, fn):
    global ball
    try: ok = bool(fn())
    except Exception as e: ok, nom = False, nom + f"  [{type(e).__name__}: {str(e)[:60]}]"
    ball += ok; natijalar.append(("✓ " if ok else "✗ ") + nom)

op1 = op_tuz(execute_calldata(ALI, E // 10))
tek("1 userOpHash: Python (userop.py) = Solidity (getUserOpHash)", lambda: ep.functions.getUserOpHash(op1.kortej()).call() == userop_hash(op1, ep.address, CHAIN))
def t2():
    ali0, bundler0 = w3.eth.get_balance(ALI), w3.eth.get_balance(BUNDLER)
    r, ev = yubor(op1)
    a = ev[0]["args"]
    print(f"   1-UserOp: handleOps gazi {r.gasUsed}, actualGasUsed {a['actualGasUsed']}, actualGasCost {a['actualGasCost'] / 1e18:.6f} ETH")
    return (w3.eth.get_balance(ALI) - ali0 == E // 10 and a["success"] and w3.eth.get_balance(EGA.address) == 0
            and w3.eth.get_balance(BUNDLER) - bundler0 + r.gasUsed * r.effectiveGasPrice == a["actualGasCost"])
tek("2 egasida 0 ETH, lekin UserOp Ali'ga 0,1 ETH yubordi; bundler kompensatsiya oldi", t2)
tek("3 nonce 0 → 1", lambda: ep.functions.getNonce(hisob.address, 0).call() == 1)
tek("4 o'sha UserOp qayta yuborilsa rad (AA25)", lambda: rad([op1], "AA25"))
tek("5 begona kalit imzosi rad (AA24)", lambda: rad([op_tuz(execute_calldata(ALI, E), kalit="0x" + "99" * 32)], "AA24"))
tek("6 akkaunt depozitidan gaz to'langan", lambda: 0 < ep.functions.balanceOf(hisob.address).call() < E)
def t7():
    t = token.functions
    approve = bytes.fromhex(t.approve(ALI, 5 * E).build_transaction({"gas": 10**6})["data"][2:])
    transfer = bytes.fromhex(t.transfer(A[2], 7 * E).build_transaction({"gas": 10**6})["data"][2:])
    _, ev = yubor(op_tuz(batch_calldata([(token.address, 0, approve), (token.address, 0, transfer)])))
    return ev[0]["args"]["success"] and t.allowance(hisob.address, ALI).call() == 5 * E and t.balanceOf(A[2]).call() == 7 * E
tek("7 executeBatch: approve + transfer bitta UserOp'da", t7)
def t8():
    t = token.functions
    approve = bytes.fromhex(t.approve(ALI, 9 * E).build_transaction({"gas": 10**6})["data"][2:])
    yomon = bytes.fromhex(t.transfer(A[2], 10**6 * E).build_transaction({"gas": 10**6})["data"][2:])   # balans yetmaydi
    _, ev = yubor(op_tuz(batch_calldata([(token.address, 0, approve), (token.address, 0, yomon)])))
    return not ev[0]["args"]["success"] and t.allowance(hisob.address, ALI).call() == 5 * E and ep.functions.getNonce(hisob.address, 0).call() == 3
tek("8 batch atomar: ikkinchi amal xato → birinchisi ham bekor, nonce baribir oshdi", t8)
tek("9 parallel nonce kaliti (key = 7) mustaqil ishlaydi",
    lambda: (yubor(op_tuz(execute_calldata(ALI, 1), key=7)), ep.functions.getNonce(hisob.address, 7).call() == (7 << 64) | 1)[1])
def t10():
    tx = homiy.functions.qosh(hisob.address, True).transact({"from": A[0]}); w3.eth.wait_for_transaction_receipt(tx)
    hisob0, homiy0 = ep.functions.balanceOf(hisob.address).call(), ep.functions.balanceOf(homiy.address).call()
    _, ev = yubor(op_tuz(execute_calldata(ALI, 1), paymasterAndData=bytes.fromhex(homiy.address[2:])))
    return (ev[0]["args"]["paymaster"] == homiy.address and ep.functions.balanceOf(hisob.address).call() == hisob0
            and homiy0 - ep.functions.balanceOf(homiy.address).call() == ev[0]["args"]["actualGasCost"])
tek("10 paymaster gazni to'ladi, akkaunt depoziti o'zgarmadi", t10)
tek("11 ro'yxatda yo'q akkaunt uchun paymaster rad (AA34)",
    lambda: (homiy.functions.qosh(hisob.address, False).transact({"from": A[0]}),
             rad([op_tuz(execute_calldata(ALI, 1), paymasterAndData=bytes.fromhex(homiy.address[2:]))], "AA34"))[1])
def t12():
    sel = Web3.keccak(text="egasiniAlmashtir(address)")[:4] + bytes(12) + bytes.fromhex(YANGI_EGA.address[2:])
    yubor(op_tuz(execute_calldata(hisob.address, 0, sel)))
    return (hisob.functions.egasi().call() == YANGI_EGA.address and rad([op_tuz(execute_calldata(ALI, 1))], "AA24")
            and yubor(op_tuz(execute_calldata(ALI, 1), kalit=YANGI_EGA.key))[1][0]["args"]["success"])
tek("12 egasini UserOp orqali almashtirish: eski kalit endi rad, yangisi ishlaydi", t12)
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")
