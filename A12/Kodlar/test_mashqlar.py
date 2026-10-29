# A14 · 15 ta avtomatik tekshiruv. O'rnatish: pip install "web3[tester]" py-solc-x
# Ishga tushirish: python test_mashqlar.py [Mashqlar_yechim.sol | Mashqlar_shablon.sol]
import sys, solcx
from web3 import Web3, EthereumTesterProvider
FAYL = sys.argv[1] if len(sys.argv) > 1 else "Mashqlar_shablon.sol"
def kompilyatsiya(fayl):
    solcx.install_solc("0.8.28")
    out = solcx.compile_files([fayl], output_values=["abi", "bin"], solc_version="0.8.28")
    return {k.split(":")[1]: v for k, v in out.items()}
B = kompilyatsiya(FAYL)
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts
def dep(n): 
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor().transact({"from": A[0]}))
    return w3.eth.contract(address=r.contractAddress, abi=B[n]["abi"])
def tx(f, frm=0, **kw): return w3.eth.wait_for_transaction_receipt(f.transact({"from": A[frm], **kw}))
def rad(f, frm=0, matn="", **kw):
    try: f.call({"from": A[frm], **kw}); return False
    except Exception as e: return matn in str(e)
ball, natijalar = 0, []
def tek(nom, shart):
    global ball; ball += bool(shart); natijalar.append(("✓" if shart else "✗") + " " + nom)
def xavfsiz(nom, fn):
    try: tek(nom, fn())
    except Exception as e: tek(nom + f"  [{type(e).__name__}]", False)

h = dep("Hisoblagich")
xavfsiz("1a oshir()", lambda: (tx(h.functions.oshir()), h.functions.son().call() == 1)[1])
xavfsiz("1b nolda kamaytir rad", lambda: (tx(h.functions.kamaytir()), rad(h.functions.kamaytir(), matn="Son nolga teng"))[1])
xavfsiz("1c event", lambda: len(h.events.Ozgardi().process_receipt(tx(h.functions.oshir()))) == 1)
t = dep("Talabalar")
xavfsiz("2a ro'yxatdan o'tish", lambda: (tx(t.functions.royxatdanOt("Ali", 2), 1), t.functions.royxat(A[1]).call()[0] == "Ali")[1])
xavfsiz("2b qayta o'tish rad", lambda: rad(t.functions.royxatdanOt("Ali", 2), 1, "Allaqachon"))
xavfsiz("2c kurs 5 rad", lambda: rad(t.functions.royxatdanOt("Vali", 5), 2, "Kurs"))
o = dep("Ovoz")
xavfsiz("3a ovozlar sanaladi", lambda: (tx(o.functions.ovozBer(True), 1), tx(o.functions.ovozBer(True), 2), tx(o.functions.ovozBer(False), 3), o.functions.ha().call() == 2)[-1])
xavfsiz("3b ikki marta ovoz rad", lambda: rad(o.functions.ovozBer(False), 1, "bergansiz"))
xavfsiz("3c faqat egasi yopadi", lambda: rad(o.functions.yakunla(), 1, "Faqat egasi") and (tx(o.functions.yakunla()), o.functions.natija().call() == "Qabul qilindi")[1])
q = dep("VaqtliQulf")
xavfsiz("4a ETH qo'yish", lambda: (tx(q.functions.qoy(3600), 1, value=10**18), q.functions.qoldiq(A[1]).call() == 10**18)[1])
xavfsiz("4b erta olish rad", lambda: rad(q.functions.ol(), 1, "Hali erta"))
def kech():
    w3.provider.ethereum_tester.time_travel(w3.eth.get_block("latest")["timestamp"] + 3601); w3.provider.ethereum_tester.mine_blocks(1)
    tx(q.functions.ol(), 1); return q.functions.qoldiq(A[1]).call() == 0 and w3.eth.get_balance(q.address) == 0
xavfsiz("4c vaqt o'tgach olish", kech)
r = dep("OqRoyxat")
xavfsiz("5a begona qo'sha olmaydi", lambda: rad(r.functions.qosh(A[2]), 1, "Faqat egasi"))
xavfsiz("5b ro'yxatsiz kirish rad", lambda: rad(r.functions.kir(), 2, "Royxatda yoq"))
xavfsiz("5c ruxsatli kiradi", lambda: (tx(r.functions.qosh(A[2])), tx(r.functions.kir(), 2), r.functions.kirishlar().call() == 1)[-1])
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/15")
