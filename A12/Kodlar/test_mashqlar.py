# A12 · 20 ta avtomatik tekshiruv (har mashqqa 4 ta). O'rnatish: pip install "web3[tester]" py-solc-x
# Ishga tushirish: python test_mashqlar.py [Mashqlar_yechim.sol | Mashqlar_shablon.sol]
import sys, solcx
from web3 import Web3, EthereumTesterProvider
FAYL = sys.argv[1] if len(sys.argv) > 1 else "Mashqlar_shablon.sol"
# 4d uchun hujumchi: receive() ichidan ol() ni qayta chaqirib, qulfdagi boshqalarning ETH'ini olishga urinadi
HUJUMCHI = """
pragma solidity ^0.8.20;
interface IQulf { function qoy(uint256 sekund) external payable; function ol() external; }
contract Hujumchi {
    IQulf public q; uint256 public marta;
    constructor(address a) { q = IQulf(a); }
    function hujum() external payable { q.qoy{value: msg.value}(0); q.ol(); }
    receive() external payable { if (marta < 5 && address(q).balance >= msg.value) { marta++; q.ol(); } }
}
"""
def kompilyatsiya(fayl):
    solcx.install_solc("0.8.28")
    out = solcx.compile_files([fayl], output_values=["abi", "bin"], solc_version="0.8.28")
    out.update(solcx.compile_source(HUJUMCHI, output_values=["abi", "bin"], solc_version="0.8.28"))
    return {k.split(":")[1]: v for k, v in out.items()}
B = kompilyatsiya(FAYL)
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; ETH = 10**18
def dep(n, *args):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor(*args).transact({"from": A[0]}))
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
xavfsiz("1b nolda kamaytir rad", lambda: (tx(h.functions.kamaytir()), h.functions.son().call() == 0 and rad(h.functions.kamaytir(), matn="Son nolga teng"))[1])
xavfsiz("1c oshir() event", lambda: [dict(e["args"]) for e in h.events.Ozgardi().process_receipt(tx(h.functions.oshir()))] == [{"kim": A[0], "yangi": 1}])
xavfsiz("1d kamaytir() event", lambda: [e["args"]["yangi"] for e in h.events.Ozgardi().process_receipt(tx(h.functions.kamaytir()))] == [0] and h.functions.son().call() == 0)
t = dep("Talabalar")
xavfsiz("2a ro'yxatdan o'tish", lambda: (tx(t.functions.royxatdanOt("Ali", 2), 1), list(t.functions.royxat(A[1]).call()) == ["Ali", 2, True])[1])
xavfsiz("2b qayta o'tish rad", lambda: rad(t.functions.royxatdanOt("Ali", 2), 1, "Allaqachon"))
xavfsiz("2c kurs 0 va 5 rad", lambda: rad(t.functions.royxatdanOt("Vali", 5), 2, "Kurs") and rad(t.functions.royxatdanOt("Vali", 0), 2, "Kurs"))
xavfsiz("2d soni va Qoshildi event", lambda: len(t.events.Qoshildi().process_receipt(tx(t.functions.royxatdanOt("Vali", 4), 2))) == 1 and t.functions.soni().call() == 2)
o = dep("Ovoz")
xavfsiz("3a ovozlar sanaladi", lambda: (tx(o.functions.ovozBer(True), 1), tx(o.functions.ovozBer(True), 2), tx(o.functions.ovozBer(False), 3), o.functions.ha().call() == 2 and o.functions.yoq().call() == 1)[-1])
xavfsiz("3b ikki marta ovoz rad", lambda: rad(o.functions.ovozBer(False), 1, "bergansiz"))
xavfsiz("3c faqat egasi yopadi", lambda: rad(o.functions.yakunla(), 1, "Faqat egasi") and (tx(o.functions.yakunla()), o.functions.yopiq().call() and o.functions.natija().call() == "Qabul qilindi")[1])
xavfsiz("3d yopilgach ovoz rad", lambda: o.functions.yopiq().call() and rad(o.functions.ovozBer(True), 4, "Ovoz yopilgan"))
q = dep("VaqtliQulf")
xavfsiz("4a ETH qo'yish, 0 ETH rad", lambda: rad(q.functions.qoy(3600), 1, "ETH yuboring") and (tx(q.functions.qoy(3600), 1, value=ETH), q.functions.qoldiq(A[1]).call() == ETH)[1])
xavfsiz("4b erta olish rad", lambda: rad(q.functions.ol(), 1, "Hali erta"))
def kech():
    w3.provider.ethereum_tester.time_travel(w3.eth.get_block("latest")["timestamp"] + 3601); w3.provider.ethereum_tester.mine_blocks(1)
    oldin = w3.eth.get_balance(A[1]); r = tx(q.functions.ol(), 1)
    qaytdi = w3.eth.get_balance(A[1]) - oldin + r.gasUsed * r.effectiveGasPrice == ETH
    return qaytdi and q.functions.qoldiq(A[1]).call() == 0 and w3.eth.get_balance(q.address) == 0 and rad(q.functions.ol(), 1, "Qoldiq yoq")
xavfsiz("4c vaqt o'tgach olish", kech)
def reentrancy():
    q2 = dep("VaqtliQulf"); tx(q2.functions.qoy(0), 1, value=4 * ETH)          # boshqa foydalanuvchining 4 ETH'i
    hj = dep("Hujumchi", q2.address)
    try: tx(hj.functions.hujum(), 5, value=ETH)                                  # to'g'ri kodda hujum revert bo'ladi
    except Exception: pass
    return q2.functions.qoldiq(A[1]).call() == 4 * ETH and w3.eth.get_balance(q2.address) >= 4 * ETH
xavfsiz("4d reentrancy hujumi muvaffaqiyatsiz", reentrancy)
r = dep("OqRoyxat")
xavfsiz("5a begona qo'sha olmaydi", lambda: rad(r.functions.qosh(A[2]), 1, "Faqat egasi"))
xavfsiz("5b ro'yxatsiz kirish rad", lambda: rad(r.functions.kir(), 2, "Royxatda yoq"))
xavfsiz("5c ruxsatli kiradi", lambda: (tx(r.functions.qosh(A[2])), tx(r.functions.kir(), 2), r.functions.ruxsat(A[2]).call() and r.functions.kirishlar().call() == 1)[-1])
xavfsiz("5d qosh() event", lambda: [e["args"]["kim"] for e in r.events.Qoshildi().process_receipt(tx(r.functions.qosh(A[3])))] == [A[3]])
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")
