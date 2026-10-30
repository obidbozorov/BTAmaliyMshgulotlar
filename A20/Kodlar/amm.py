# A20 · Doimiy ko'paytma (x · y = k) bozor-maker modeli — Uniswap V2 formulalari, butun sonli arifmetika
# MiniAMM.sol aynan shu formulalarni ishlatadi; test_amm.py ikkalasini bir-biri bilan solishtiradi.
from math import isqrt

MIN_LIKVIDLIK = 1000          # birinchi LP tokenlarning bir qismi abadiy qulflanadi (bo'lish hujumidan himoya)
KOMISSIYA = 3                 # 3/1000 = 0,3%


class Rad(Exception):
    """Solidity'dagi revert o'xshashi (assert emas: python -O uni o'chirib yuboradi — A6 ga qarang)"""


def chiqish_miqdori(kirish: int, zaxira_kirish: int, zaxira_chiqish: int) -> int:
    """Uniswap V2 getAmountOut: komissiya kiruvchi tokendan olinadi, natija pastga yaxlitlanadi"""
    if kirish <= 0 or zaxira_kirish <= 0 or zaxira_chiqish <= 0:
        raise Rad("Miqdor yoki zaxira nol")
    k = kirish * (1000 - KOMISSIYA)
    return k * zaxira_chiqish // (zaxira_kirish * 1000 + k)


class Havza:
    def __init__(self):
        self.x = self.y = 0               # A va B token zaxiralari
        self.lp_jami = 0
        self.lp = {}                      # kim → LP token

    def narx(self) -> float:
        """1 A token necha B token turadi (spot narx)"""
        return self.y / self.x

    def likvidlik_qosh(self, kim, dx: int, dy: int) -> int:
        if self.lp_jami == 0:
            lp = isqrt(dx * dy) - MIN_LIKVIDLIK
            self.lp_jami = MIN_LIKVIDLIK          # 0x0 manziliga qulflangan
        else:
            lp = min(dx * self.lp_jami // self.x, dy * self.lp_jami // self.y)
        if lp <= 0:
            raise Rad("LP nol")
        self.x += dx; self.y += dy
        self.lp_jami += lp; self.lp[kim] = self.lp.get(kim, 0) + lp
        return lp

    def likvidlik_ol(self, kim, lp: int):
        dx, dy = lp * self.x // self.lp_jami, lp * self.y // self.lp_jami
        self.lp[kim] -= lp; self.lp_jami -= lp
        self.x -= dx; self.y -= dy
        return dx, dy

    def almashtir(self, kirish: int, a_dan_b_ga=True, min_chiqish=0) -> int:
        if a_dan_b_ga:
            out = chiqish_miqdori(kirish, self.x, self.y)
            if out < min_chiqish:
                raise Rad("Slippage: chiqish kam")
            self.x += kirish; self.y -= out
        else:
            out = chiqish_miqdori(kirish, self.y, self.x)
            if out < min_chiqish:
                raise Rad("Slippage: chiqish kam")
            self.y += kirish; self.x -= out
        return out
