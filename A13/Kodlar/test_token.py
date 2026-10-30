# A13 · Token.sol uchun 12 ta avtomatik tekshiruv (mahalliy EVM, internet faqat solc yuklash uchun)
# O'rnatish: pip install -r requirements.txt   ·   Ishga tushirish: python test_token.py [Token.sol]
# Ixtiyoriy: python test_token.py Token.sol --oz <node_modules yo'li>  — OpenZeppelin versiyasi bilan gaz qiyosi
import sys, solcx
from web3 import Web3, EthereumTesterProvider
FAYL = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "Token.sol"
solcx.install_solc("0.8.28")
def kompilyatsiya(fayl, nom, **kw):
    out = solcx.compile_files([fayl], output_values=["abi", "bin"], solc_version="0.8.28", **kw)
    return out[f"{fayl}:{nom}"]
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18; MAX = 2**256 - 1
def dep(k, *args):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=k["abi"], bytecode=k["bin"]).constructor(*args).transact({"from": A[0]}))
    return w3.eth.contract(address=r.contractAddress, abi=k["abi"]), r.gasUsed
def tx(f, frm=0): return w3.eth.wait_for_transaction_receipt(f.transact({"from": A[frm]}))
def rad(f, frm=0, matn=""):
    try: f.call({"from": A[frm]}); return False
    except Exception as e: return matn in str(e)
ball, natijalar = 0, []
def tek(nom, fn):
    global ball
    try: ok = bool(fn())
    except Exception as e: ok, nom = False, nom + f"  [{type(e).__name__}]"
    ball += ok; natijalar.append(("✓ " if ok else "✗ ") + nom)

t, deploy_gaz = dep(kompilyatsiya(FAYL, "Token"), 1000)
f = t.functions
tek("1 name / symbol / decimals", lambda: (f.name().call(), f.symbol().call(), f.decimals().call()) == ("ProfiCoin", "PRC", 18))
tek("2 totalSupply = 1000 PRC, hammasi egada", lambda: f.totalSupply().call() == 1000 * E == f.balanceOf(A[0]).call())
def t3():
    r = tx(f.transfer(A[1], 25 * E)); ev = t.events.Transfer().process_receipt(r)
    print(f"   transfer gazi: {r.gasUsed}")
    return f.balanceOf(A[1]).call() == 25 * E and [dict(e["args"]) for e in ev] == [{"from": A[0], "to": A[1], "value": 25 * E}]
tek("3 transfer + Transfer event", t3)
tek("4 balansdan ko'p transfer rad", lambda: rad(f.transfer(A[2], 26 * E), 1, "Balans yetarli emas"))
tek("5 0x0 manziliga transfer rad", lambda: rad(f.transfer("0x" + "00" * 20, 1), 0, "Manzil bosh"))
def t6():
    r = tx(f.approve(A[2], 10 * E), 1); ev = t.events.Approval().process_receipt(r)
    print(f"   approve gazi : {r.gasUsed}")
    return f.allowance(A[1], A[2]).call() == 10 * E and ev[0]["args"]["spender"] == A[2]
tek("6 approve + Approval event", t6)
tek("7 transferFrom ruxsat doirasida, allowance kamayadi",
    lambda: (tx(f.transferFrom(A[1], A[3], 4 * E), 2), f.balanceOf(A[3]).call() == 4 * E and f.allowance(A[1], A[2]).call() == 6 * E)[1])
tek("8 ruxsatdan ortiq transferFrom rad", lambda: rad(f.transferFrom(A[1], A[3], 7 * E), 2, "Ruxsat yetarli emas"))
tek("9 cheksiz ruxsat kamaytirilmaydi",
    lambda: (tx(f.approve(A[2], MAX)), tx(f.transferFrom(A[0], A[4], E), 2), f.allowance(A[0], A[2]).call() == MAX)[2])
tek("10 mint faqat egasi", lambda: rad(f.mint(A[1], E), 1, "Faqat egasi") and (tx(f.mint(A[5], 5 * E)), f.totalSupply().call() == 1005 * E)[1])
tek("11 burn totalSupply'ni kamaytiradi", lambda: (tx(f.burn(2 * E), 5), f.totalSupply().call() == 1003 * E and f.balanceOf(A[5]).call() == 3 * E)[1])
tek("12 invariant: balanslar yig'indisi = totalSupply", lambda: sum(f.balanceOf(a).call() for a in A) == f.totalSupply().call())
print(f"   deploy gazi  : {deploy_gaz}")
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")

if "--oz" in sys.argv:                                   # OpenZeppelin versiyasi bilan gaz qiyosi
    nm = sys.argv[sys.argv.index("--oz") + 1]
    k = kompilyatsiya("TokenOZ.sol", "TokenOZ", import_remappings=[f"@openzeppelin/={nm}/@openzeppelin/"], allow_paths=[nm])
    oz, oz_deploy = dep(k, 1000)
    r = tx(oz.functions.transfer(A[1], 25 * E))
    print(f"\nOpenZeppelin TokenOZ: deploy {oz_deploy} gaz, transfer {r.gasUsed} gaz, symbol {oz.functions.symbol().call()}")
