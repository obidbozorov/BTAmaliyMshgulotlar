# A7 · 2-skript: explorer'dagi “Input Data” ni o'qish — funksiya selektori va parametrlar
# O'rnatish: pip install pycryptodome
from Crypto.Hash import keccak

def selektor(imzo: str) -> str:
    h = keccak.new(digest_bits=256); h.update(imzo.encode()); return h.hexdigest()[:8]

MALUM = {selektor(s): s for s in ["transfer(address,uint256)", "approve(address,uint256)",
         "transferFrom(address,address,uint256)", "setApprovalForAll(address,bool)", "balanceOf(address)"]}

def ochish(input_hex: str):
    d = input_hex.removeprefix("0x")
    sel, args = d[:8], d[8:]
    imzo = MALUM.get(sel, "noma'lum")
    print(f"Selektor 0x{sel} → {imzo}")
    for i in range(0, len(args), 64):
        bolak = args[i:i+64]
        print(f"  parametr {i//64}: 0x{bolak}")
    return imzo, [args[i:i+64] for i in range(0, len(args), 64)]

if __name__ == "__main__":
    for s, imzo in MALUM.items(): print(f"0x{s}  {imzo}")
    print()
    # 0x7099…79C8 manziliga 25 PRC (18 kasr) o'tkazish
    kirish = ("0xa9059cbb"
              "00000000000000000000000070997970c51812dc3a010c7d01b50e0d17dc79c8"
              "0000000000000000000000000000000000000000000000015af1d78b58c40000")
    imzo, p = ochish(kirish)
    print("  → kimga :", "0x" + p[0][24:])
    print("  → miqdor:", int(p[1], 16) / 10**18, "PRC")
    print()
    cheksiz = "0x095ea7b3" + "0"*24 + "70997970c51812dc3a010c7d01b50e0d17dc79c8" + "f"*64
    imzo, p = ochish(cheksiz)
    print("  → ruxsat miqdori 2^256−1 ga tengmi?", int(p[1], 16) == 2**256 - 1, "— CHEKSIZ approve!")
