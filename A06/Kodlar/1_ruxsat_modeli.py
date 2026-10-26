"""A8 | ERC-20 approve, allowance, transferFrom va revoke - to'liq oflayn model.
Bu haqiqiy token yoki tarmoq emas; xavfsizlik mashqi uchun soddalashtirilgan model.
"""
from dataclasses import dataclass, field

MAX_UINT256 = 2**256 - 1

@dataclass
class TestToken:
    balances: dict[str, int] = field(default_factory=dict)
    allowances: dict[tuple[str, str], int] = field(default_factory=dict)

    def approve(self, owner: str, spender: str, amount: int):
        assert 0 <= amount <= MAX_UINT256
        self.allowances[(owner, spender)] = amount
        print(f"Approval: owner={owner}, spender={spender}, amount={amount}")

    def allowance(self, owner: str, spender: str) -> int:
        return self.allowances.get((owner, spender), 0)

    def transfer_from(self, spender: str, owner: str, receiver: str, amount: int):
        assert amount >= 0
        assert self.balances.get(owner, 0) >= amount, "Balans yetarli emas"
        permission = self.allowance(owner, spender)
        assert permission >= amount, "Ruxsat yetarli emas"
        self.balances[owner] -= amount
        self.balances[receiver] = self.balances.get(receiver, 0) + amount
        # Ayrim ERC-20 amaliyotlarida maxUint ruxsat kamaytirilmaydi.
        if permission != MAX_UINT256:
            self.allowances[(owner, spender)] -= amount
        print(f"transferFrom: spender={spender} -> {receiver}, amount={amount}")


def main():
    token = TestToken(balances={"Talaba": 1000, "Qabul qiluvchi": 0})
    print("=== 1. Chegaralangan ruxsat ===")
    token.approve("Talaba", "DEX", 120)
    token.transfer_from("DEX", "Talaba", "Qabul qiluvchi", 50)
    print("Qolgan ruxsat:", token.allowance("Talaba", "DEX"))
    print("=== 2. Cheksiz ruxsat (xavfli!) ===")
    token.approve("Talaba", "ShubhaliSpender", MAX_UINT256)
    print("Cheksizmi?", token.allowance("Talaba", "ShubhaliSpender") == MAX_UINT256)
    print("=== 3. Ruxsatni bekor qilish ===")
    token.approve("Talaba", "ShubhaliSpender", 0)
    try:
        token.transfer_from("ShubhaliSpender", "Talaba", "Qabul qiluvchi", 1)
    except AssertionError as exc:
        print("Kutilgan rad javobi:", exc)
    print("Yakuniy balanslar:", token.balances)

if __name__ == "__main__":
    main()
