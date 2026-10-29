"""A6 | Tranzaksiya sarlavhalariga asoslangan himoyaviy indikatorlar tahlili.
Barcha yozuvlar SUN'IY; manzillar haqiqiy foydalanuvchilarga tegishli emas.
"""
from dataclasses import dataclass

SELECTORS = {
    "0x095ea7b3": "approve(address,uint256)",
    "0xa22cb465": "setApprovalForAll(address,bool)",
    "0xa9059cbb": "transfer(address,uint256)",
    "0x23b872dd": "transferFrom(address,address,uint256)",
}
MAX_UINT256 = 2**256-1

@dataclass(frozen=True)
class Ssenariy:
    nom: str
    selector: str
    spender_tanish: bool
    miqdor: int
    sayt_nomi: str
    domain_mos: bool
    oddiy_xabar: bool = False

MISOLLAR = [
    Ssenariy("A: tanish DEX", "0x095ea7b3", True, 25, "dex.example", True),
    Ssenariy("B: soxta bonus", "0x095ea7b3", False, MAX_UINT256, "claim-b0nus.example", False),
    Ssenariy("C: NFT ruxsati", "0xa22cb465", False, 1, "nft-airdrop.example", False),
    Ssenariy("D: oddiy o'tkazma", "0xa9059cbb", True, 10, "wallet.example", True),
    Ssenariy("E: soxta imzo oynasi", "0x095ea7b3", False, MAX_UINT256, "reward.example", False, True),
]

def tahlil(s: Ssenariy):
    ball = 0
    sabablar = []
    if not s.domain_mos:
        ball += 3; sabablar.append("domen tasdiqlanmagan")
    if not s.spender_tanish:
        ball += 3; sabablar.append("spender noma'lum")
    if s.selector == "0x095ea7b3" and s.miqdor == MAX_UINT256:
        ball += 4; sabablar.append("cheksiz ERC-20 allowance")
    if s.selector == "0xa22cb465" and s.miqdor == 1:
        ball += 4; sabablar.append("butun NFT kolleksiyasiga ruxsat")
    if s.oddiy_xabar:
        ball += 2; sabablar.append("imzo va tranzaksiya chalkashgan")
    daraja = "YUQORI" if ball >= 7 else "O'RTA" if ball >= 3 else "PAST"
    return daraja, ball, sabablar

if __name__ == "__main__":
    print("TAHLIL: indikatorlar bahosi, firibgarlikning isboti emas.\n")
    for s in MISOLLAR:
        daraja, ball, sabablar = tahlil(s)
        print(f"{s.nom}: {SELECTORS[s.selector]}  -> {daraja} ({ball}/16)")
        print("  Sabablar:", "; ".join(sabablar) or "bu indikatorlarda xavf aniqlanmadi")
