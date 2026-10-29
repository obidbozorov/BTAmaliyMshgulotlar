# A20 · MiniAMM.sol uchun 12 ta avtomatik tekshiruv — Solidity natijalari Python modeli (amm.py) bilan aynan solishtiriladi
# Ishga tushirish: python test_amm.py
import random, solcx
from math import isqrt
from web3 import Web3, EthereumTesterProvider
from amm import Havza, chiqish_miqdori, MIN_LIKVIDLIK

solcx.install_solc("0.8.28")
B = {k.split(":")[1]: v for k, v in solcx.compile_files(["MiniAMM.sol", "Tanga.sol"], output_values=["abi", "bin"], solc_version="0.8.28").items()}
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18; KECH = 2**40
def dep(n, *a):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor(*a).transact({"from": A[0]}))
    return w3.eth.contract(address=r.contractAddress, abi=B[n]["abi"])
def tx(f, frm=0): return w3.eth.wait_for_transaction_receipt(f.transact({"from": A[frm]}))
def rad(f, frm=0, matn=""):
    try: f.call({"from": A[frm]}); return False
    except Exception as e: return matn in str(e)
ball, natijalar = 0, []
def tek(nom, fn):
    global ball
    try: ok = bool(fn())
    except Exception as e: ok, nom = False, nom + f"  [{type(e).__name__}: {str(e)[:60]}]"
    ball += ok; natijalar.append(("✓ " if ok else "✗ ") + nom)

eth, usd = dep("Tanga", "Sinov ETH", "sETH"), dep("Tanga", "Sinov USD", "sUSD")
amm = dep("MiniAMM", eth.address, usd.address); f = amm.functions
for i in range(6):                                         # har bir hisobga token va ruxsat
    tx(eth.functions.kran(1000 * E), i); tx(usd.functions.kran(1_000_000 * E), i)
    tx(eth.functions.approve(amm.address, 2**256 - 1), i); tx(usd.functions.approve(amm.address, 2**256 - 1), i)
zax = lambda: (f.zaxiraA().call(), f.zaxiraB().call())
model = Havza()

def t1():
    tx(f.likvidlikQosh(100 * E, 300_000 * E, KECH)); lp = model.likvidlik_qosh(A[0], 100 * E, 300_000 * E)
    return f.lpBalans(A[0]).call() == lp == isqrt(100 * E * 300_000 * E) - MIN_LIKVIDLIK and f.lpJami().call() == model.lp_jami
tek("1 birinchi likvidlik: LP = √(a·b) − 1000", t1)
def t2_3():
    random.seed(2026); k_osdi = True
    for _ in range(20):
        a_dan_b = random.random() < 0.5
        kirish = random.randint(1, 5 * E) if a_dan_b else random.randint(1, 15_000 * E)
        k0 = zax()[0] * zax()[1]
        tx(f.almashtir(a_dan_b, kirish, 0, KECH), 1)
        model.almashtir(kirish, a_dan_b)
        k_osdi &= zax()[0] * zax()[1] >= k0
        if zax() != (model.x, model.y): return False, False
    return True, k_osdi
natija = t2_3()
tek("2 20 ta tasodifiy almashinuv: Solidity = Python modeli (wei aniqligida)", lambda: natija[0])
tek("3 har bir almashinuvdan keyin k kamaymadi", lambda: natija[1])
tek("4 slippage: minChiqish dan kam bo'lsa rad", lambda: rad(f.almashtir(True, E, chiqish_miqdori(E, *zax()) + 1, KECH), 2, "Slippage"))
tek("5 muddati o'tgan tranzaksiya rad", lambda: rad(f.almashtir(True, E, 0, 1), 2, "Muddat otgan"))
tek("6 nol miqdor rad", lambda: rad(f.almashtir(True, 0, 0, KECH), 2, "nol"))
def t7():
    a, b = zax(); tx(f.likvidlikQosh(10 * E, 10 * E * b // a, KECH), 3)
    lp = model.likvidlik_qosh(A[3], 10 * E, 10 * E * b // a)
    return f.lpBalans(A[3]).call() == lp and zax() == (model.x, model.y)
tek("7 ikkinchi LP: ulush mavjud nisbatga proporsional", t7)
def t8():
    a, b = zax(); jami = f.lpJami().call()
    tx(f.likvidlikQosh(10 * E, 10 * E * b // a * 2, KECH), 4)                # B token ikki baravar ko'p berildi
    return f.lpBalans(A[4]).call() == 10 * E * jami // a
tek("8 nisbat buzilsa — LP kichik tomon bo'yicha (ortiqchasi havzaga qoladi)", t8)
tek("9 egasidan ko'p LP olib bo'lmaydi", lambda: rad(f.likvidlikOl(f.lpBalans(A[3]).call() + 1, 0, 0, KECH), 3, "LP yetarli emas"))
def t10():
    lp = f.lpBalans(A[3]).call(); a, b = zax(); jami = f.lpJami().call()
    e0, u0 = eth.functions.balanceOf(A[3]).call(), usd.functions.balanceOf(A[3]).call()
    tx(f.likvidlikOl(lp, 0, 0, KECH), 3)
    return eth.functions.balanceOf(A[3]).call() - e0 == lp * a // jami and usd.functions.balanceOf(A[3]).call() - u0 == lp * b // jami
tek("10 likvidlikni olish: ulushga mos A va B qaytadi", t10)
def t11():
    lp = f.lpBalans(A[0]).call(); jami0 = f.lpJami().call(); k0 = zax()[0] * zax()[1]
    for i in range(30): tx(f.almashtir(i % 2 == 0, E if i % 2 == 0 else 3000 * E, 0, KECH), 5)
    return isqrt(zax()[0] * zax()[1]) * jami0 > isqrt(k0) * f.lpJami().call()
tek("11 komissiya: savdolardan keyin 1 LP ortidagi √k oshdi", t11)
def t12():
    qurbon = 10_000 * E
    a, b = zax(); halol = chiqish_miqdori(qurbon, b, a); minimal = halol * 99 // 100   # qurbon: 1% slippage
    hujum = 1_500 * E
    e0 = eth.functions.balanceOf(A[2]).call(); u0 = usd.functions.balanceOf(A[2]).call()
    tx(f.almashtir(False, hujum, 0, KECH), 2)                                          # front-run
    olindi = f.almashtir(False, qurbon, minimal, KECH).call({"from": A[1]}); tx(f.almashtir(False, qurbon, minimal, KECH), 1)
    tx(f.almashtir(True, eth.functions.balanceOf(A[2]).call() - e0, 0, KECH), 2)        # back-run
    foyda = usd.functions.balanceOf(A[2]).call() - u0
    print(f"   sendvich: qurbon {olindi / E:.4f} ETH oldi (hujumsiz {halol / E:.4f}), hujumchi foydasi {foyda / E:,.2f} sUSD")
    return foyda > 0 and minimal <= olindi < halol
tek("12 sendvich: 1% slippage ichida hujumchi foyda oladi", t12)
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")
