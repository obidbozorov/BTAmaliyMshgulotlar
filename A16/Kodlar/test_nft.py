# A16 · NFT.sol uchun 12 ta avtomatik tekshiruv. Ishga tushirish: python test_nft.py [NFT.sol]
import sys, solcx
from web3 import Web3, EthereumTesterProvider
FAYL = sys.argv[1] if len(sys.argv) > 1 else "NFT.sol"
# safeTransferFrom sinovi uchun ikki yordamchi kontrakt: biri NFT ni qabul qiladi, biri — yo'q
YORDAMCHI = """
pragma solidity ^0.8.20;
contract Qabul { function onERC721Received(address, address, uint256, bytes calldata) external pure returns (bytes4) {
    return this.onERC721Received.selector; } }
contract Bosh {}
"""
solcx.install_solc("0.8.28")
B = {k.split(":")[1]: v for k, v in solcx.compile_files([FAYL], output_values=["abi", "bin"], solc_version="0.8.28").items()}
B.update({k.split(":")[1]: v for k, v in solcx.compile_source(YORDAMCHI, output_values=["abi", "bin"], solc_version="0.8.28").items()})
w3 = Web3(EthereumTesterProvider()); A = w3.eth.accounts
def dep(n):
    r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=B[n]["abi"], bytecode=B[n]["bin"]).constructor().transact({"from": A[0]}))
    return w3.eth.contract(address=r.contractAddress, abi=B[n]["abi"])
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

n = dep("NFT"); f = n.functions
URI = "ipfs://bafkreic5kfh53rhplch2itrhlmu36feq37appwnhtwcrycx6mrbcfnfdqq"
tek("1 ERC-165: ERC-721 va Metadata interfeyslari", lambda: f.supportsInterface(bytes.fromhex("80ac58cd")).call()
    and f.supportsInterface(bytes.fromhex("5b5e139f")).call() and not f.supportsInterface(bytes.fromhex("ffffffff")).call())
def t2():
    r = tx(f.mint(A[1], URI)); ev = n.events.Transfer().process_receipt(r)[0]["args"]
    print(f"   mint gazi: {r.gasUsed}")
    return (ev["from"], ev["to"], ev["tokenId"]) == ("0x" + "00" * 20, A[1], 1) and f.ownerOf(1).call() == A[1]
tek("2 mint: Transfer(0x0 → Ali, 1), ownerOf(1) = Ali", t2)
tek("3 tokenURI va balanceOf", lambda: f.tokenURI(1).call() == URI and f.balanceOf(A[1]).call() == 1)
tek("4 begona mint qila olmaydi", lambda: rad(f.mint(A[2], URI), 1, "Faqat egasi"))
tek("5 mavjud bo'lmagan token: ownerOf rad", lambda: rad(f.ownerOf(99), 0, "Token yoq"))
tek("6 egasi transfer qiladi", lambda: (tx(f.transferFrom(A[1], A[2], 1), 1), f.ownerOf(1).call() == A[2] and f.balanceOf(A[1]).call() == 0)[1])
tek("7 begona transfer qila olmaydi", lambda: rad(f.transferFrom(A[2], A[3], 1), 3, "Ruxsat yoq"))
tek("8 approve: ruxsat olgan o'tkazadi, ruxsat bekor bo'ladi",
    lambda: (tx(f.approve(A[3], 1), 2), tx(f.transferFrom(A[2], A[4], 1), 3), f.ownerOf(1).call() == A[4]
             and f.getApproved(1).call() == "0x" + "00" * 20)[2])
tek("9 setApprovalForAll: operator butun kolleksiyani boshqaradi",
    lambda: (tx(f.mint(A[4], URI)), tx(f.setApprovalForAll(A[5], True), 4), tx(f.transferFrom(A[4], A[5], 2), 5),
             f.ownerOf(2).call() == A[5] and f.isApprovedForAll(A[4], A[5]).call())[3])
q, b = dep("Qabul"), dep("Bosh")
tek("10 safeTransferFrom: qabul qiluvchi kontraktga o'tadi",
    lambda: (tx(f.safeTransferFrom(A[5], q.address, 2), 5), f.ownerOf(2).call() == q.address)[1])
tek("11 safeTransferFrom: qabul qilmaydigan kontraktga rad", lambda: rad(f.safeTransferFrom(A[4], b.address, 1), 4))
def t12():
    for _ in range(98): tx(f.mint(A[6], URI))
    return f.jami().call() == 100 and rad(f.mint(A[6], URI), 0, "Emissiya tugagan")
tek("12 MAKS = 100 dan ortiq chiqarib bo'lmaydi", t12)
print("\n".join(natijalar)); print(f"\nNATIJA: {ball}/{len(natijalar)}")
