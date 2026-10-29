# A21 · DAO.sol uchun 12 ta avtomatik tekshiruv. A'zolar — A3 dagi guruh ro'yxati (azolar.txt)
# Ishga tushirish: python test_dao.py
import solcx
from web3 import Web3, EthereumTesterProvider
from merkle import barg, daraxt_qur, proof_ol, royxatni_oqi

A3_ROOT = "0x2d488248a8dfeb7c2bb56400073cb8627a84f84a24fba5b1a809a10748d2fbed"     # A3 javoblar kalitidagi root
A3_PROOF = ["0x98c307bdec62d81a71972abb8c71fd9687ba40f08c52b11b930e270290f90fa2",    # A3 mening_proofim.json (1-manzil)
            "0xc8d93a34e5f93c6394354245bdb96c4b5f4228bfca47a67c71c1fe200c8935c1",
            "0x3c29e91c6629d3721873c6c73127352ead61f6922112dca9a37ab7a92a9ae21d"]
KUN = 86400; YOQ, HA, BETARAF = 0, 1, 2

solcx.install_solc("0.8.28")
k = solcx.compile_files(["DAO.sol"], output_values=["abi", "bin"], solc_version="0.8.28")["DAO.sol:DAO"]
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts; E = 10**18
azolar = royxatni_oqi(); d = daraxt_qur([barg(m) for m in azolar]); root = d[-1][0]
P = {azolar[i].lower(): ["0x" + x.hex() for x in proof_ol(d, i)] for i in range(len(azolar))}
pf = lambda a: P.get(a.lower(), [])
r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=k["abi"], bytecode=k["bin"]).constructor(root, 3 * KUN, KUN, 3).transact({"from": A[0]}))
dao = w3.eth.contract(address=r.contractAddress, abi=k["abi"]); f = dao.functions
w3.eth.wait_for_transaction_receipt(w3.eth.send_transaction({"from": A[9], "to": dao.address, "value": 5 * E}))   # xazinaga 5 ETH
def tx(fn, frm=0): return w3.eth.wait_for_transaction_receipt(fn.transact({"from": A[frm]}))
def rad(fn, frm=0, matn=""):
    try: fn.call({"from": A[frm]}); return False
    except Exception as e: return matn in str(e)
def vaqt(soniya):
    w3.provider.ethereum_tester.time_travel(w3.eth.get_block("latest")["timestamp"] + soniya); w3.provider.ethereum_tester.mine_blocks(1)
def taklif(tavsif, kimga, qiymat, frm=1):
    tx(f.taklifKirit(tavsif, kimga, qiymat, b"", pf(A[frm])), frm); return f.takliflarSoni().call() - 1
ball, natijalar = 0, []
def tek(nom, fn):
    global ball
    try: ok = bool(fn())
    except Exception as e: ok, nom = False, nom + f"  [{type(e).__name__}: {str(e)[:60]}]"
    ball += ok; natijalar.append(("✓ " if ok else "✗ ") + nom)

tek("1 Merkle root A3 dagi bilan bir xil", lambda: "0x" + root.hex() == A3_ROOT)
tek("2 A3 da olingan proof bilan a'zolik zanjirda tasdiqlanadi", lambda: f.azomi(A[0], A3_PROOF).call())
tek("3 ro'yxatda yo'q manzil taklif kirita olmaydi", lambda: not f.azomi(A[5], pf(A[0])).call()
    and rad(f.taklifKirit("x", A[6], 0, b"", pf(A[0])), 5, "Azo emas"))
t0 = taklif("Hackathon g'olibiga 1 ETH", A[6], E)
tek("4 a'zo taklif kiritdi", lambda: f.takliflar(t0).call()[0] == A[1] and f.holat(t0).call() == 0)
tek("5 ovozlar sanaladi: 2 ha, 1 yo'q", lambda: (tx(f.ovozBer(t0, HA, pf(A[0])), 0), tx(f.ovozBer(t0, HA, pf(A[1])), 1),
    tx(f.ovozBer(t0, YOQ, pf(A[2])), 2), f.takliflar(t0).call()[6:8] == [2, 1])[-1])
tek("6 ikki marta ovoz berib bo'lmaydi", lambda: rad(f.ovozBer(t0, HA, pf(A[0])), 0, "Allaqachon"))
tek("7 boshqa a'zoning proof'i bilan kirib bo'lmaydi", lambda: rad(f.ovozBer(t0, HA, pf(A[3])), 4, "Azo emas"))
tek("8 ovoz davomida bajarib bo'lmaydi", lambda: rad(f.bajar(t0), 5, "Ijroga tayyor emas"))
tek("9 muddat tugagach: kechikish davri (holat 2), hali bajarilmaydi",
    lambda: (vaqt(3 * KUN), f.holat(t0).call() == 2 and rad(f.bajar(t0), 5, "Ijroga tayyor emas"))[1])
def t10():
    vaqt(KUN); oldin = w3.eth.get_balance(A[6])
    tx(f.bajar(t0), 5)                                         # istalgan kishi ijro eta oladi
    return w3.eth.get_balance(A[6]) - oldin == E and f.holat(t0).call() == 4 and rad(f.bajar(t0), 5, "Ijroga tayyor emas")
tek("10 kechikishdan keyin ijro: xazinadan 1 ETH yuborildi, qayta ijro yo'q", t10)
tek("11 yopilgan taklifga ovoz berib bo'lmaydi", lambda: rad(f.ovozBer(t0, HA, pf(A[3])), 3, "Ovoz yopilgan"))
def t12():
    t1 = taklif("Kvorumsiz taklif", A[6], E)
    t2 = taklif("Ko'pchilik qarshi", A[6], E)
    tx(f.ovozBer(t1, HA, pf(A[0])), 0); tx(f.ovozBer(t1, HA, pf(A[1])), 1)               # 2 ovoz < kvorum 3
    for i, o in enumerate([HA, YOQ, YOQ]): tx(f.ovozBer(t2, o, pf(A[i])), i)
    vaqt(5 * KUN)
    return f.holat(t1).call() == 1 and f.holat(t2).call() == 1 and rad(f.bajar(t1), 5) and w3.eth.get_balance(dao.address) == 4 * E
tek("12 kvorum yetmasa yoki “yo'q” ko'p bo'lsa — rad (holat 1), xazina o'zgarmaydi", t12)
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")
