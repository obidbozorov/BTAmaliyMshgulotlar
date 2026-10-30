# A17 · ChiptaSotuvi.sol uchun 10 ta avtomatik tekshiruv (MockNarx bilan). Ishga tushirish: python test_oracle.py
import solcx
from web3 import Web3, EthereumTesterProvider
solcx.install_solc("0.8.28")
B = {k.split(":")[1]: v for k, v in solcx.compile_files(["ChiptaSotuvi.sol", "MockNarx.sol"],
     output_values=["abi", "bin"], solc_version="0.8.28").items()}
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18
def dep(n, *a):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor(*a).transact({"from": A[0]}))
    return w3.eth.contract(address=r.contractAddress, abi=B[n]["abi"])
def tx(f, frm=0, **kw): return w3.eth.wait_for_transaction_receipt(f.transact({"from": A[frm], **kw}))
def rad(f, frm=0, matn="", **kw):
    try: f.call({"from": A[frm], **kw}); return False
    except Exception as e: return matn in str(e)
ball, natijalar = 0, []
def tek(nom, fn):
    global ball
    try: ok = bool(fn())
    except Exception as e: ok, nom = False, nom + f"  [{type(e).__name__}]"
    ball += ok; natijalar.append(("✓ " if ok else "✗ ") + nom)

mock = dep("MockNarx", 8, 2000 * 10**8)                    # Chainlink kabi 8 kasr: 1 ETH = $2000
s = dep("ChiptaSotuvi", mock.address, 5 * E, 3600)          # chipta $5, narx 1 soatdan eski bo'lmasin
f = s.functions
tek("1 ethNarxi: 2000·10⁸ (8 kasr) → 2000·10¹⁸", lambda: f.ethNarxi().call()[0] == 2000 * E)
tek("2 $5 chipta = 0,0025 ETH", lambda: f.kerakliWei().call() == E // 400)
tek("3 aniq summa bilan sotib olish", lambda: (tx(f.sotibOl(), 1, value=E // 400), f.chiptalar(A[1]).call() == 1)[1])
tek("4 kam ETH rad etiladi", lambda: rad(f.sotibOl(), 2, "ETH yetarli emas", value=E // 400 - 1))
def t5():
    oldin = w3.eth.get_balance(A[2]); r = tx(f.sotibOl(), 2, value=E // 100)        # 0,01 ETH yuboradi
    sarf = oldin - w3.eth.get_balance(A[2]) - r.gasUsed * r.effectiveGasPrice
    return sarf == E // 400 and w3.eth.get_balance(s.address) == 2 * E // 400
tek("5 ortiqcha ETH qaytariladi", t5)
tek("6 narx $2500 bo'lsa — 0,002 ETH", lambda: (tx(mock.functions.narxniOrnat(2500 * 10**8)), f.kerakliWei().call() == E // 500)[1])
tek("7 eskirgan narx rad etiladi", lambda: (tx(mock.functions.yoshiniOrnat(7200)), rad(f.sotibOl(), 1, "Narx eskirgan", value=E))[1])
tek("8 nol yoki manfiy narx rad etiladi", lambda: (tx(mock.functions.narxniOrnat(-1)), rad(f.kerakliWei(), 0, "Narx notogri"))[1])
def t9():
    m18 = dep("MockNarx", 18, 2000 * E); s18 = dep("ChiptaSotuvi", m18.address, 5 * E, 3600)
    return s18.functions.kerakliWei().call() == E // 400
tek("9 18 kasrli manba bilan ham bir xil natija", t9)
def t10():
    if not rad(f.yechib(A[3]), 3, "Faqat egasi"): return False
    oldin = w3.eth.get_balance(A[4]); tx(f.yechib(A[4]))
    return w3.eth.get_balance(A[4]) - oldin == 2 * E // 400 and w3.eth.get_balance(s.address) == 0
tek("10 yechib: faqat egasi, butun balans", t10)
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")
