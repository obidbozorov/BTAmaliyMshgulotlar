"""A11 | Validator iqtisodiyoti, o'quv FARAZLARI asosida.
Bu Ethereum konsensus protokoli mukofotlarini aniq bashorat qilmaydi.
Kiritmalarni talaba o'zi tahrirlashi mumkin.
"""
from dataclasses import dataclass

@dataclass
class Faraz:
    stake_eth: float = 32.0
    yillik_nominal_reward_pct: float = 3.0
    uptime_pct: float = 98.0
    bekor_qolgan_vaqt_penalty_eth: float = 0.025
    infratuzilma_yillik_eth: float = 0.12
    slash_ehtimoli_pct: float = 0.2  # o'quv shartli ehtimol
    slash_zarar_eth: float = 1.0    # o'quv shartli zarar


def hisob(f: Faraz):
    assert f.stake_eth > 0 and 0 <= f.uptime_pct <= 100
    gross = f.stake_eth*f.yillik_nominal_reward_pct/100 * f.uptime_pct/100
    expected_slash = f.slash_ehtimoli_pct/100 * f.slash_zarar_eth
    net = gross - f.bekor_qolgan_vaqt_penalty_eth - f.infratuzilma_yillik_eth - expected_slash
    return gross, expected_slash, net, net/f.stake_eth*100

if __name__ == "__main__":
    print("FARAZLAR: 32 ETH, 3% nominal stavka, 0.12 ETH xarajat/yil")
    print("Uptime | bruto ETH | kutilgan slash | sof ETH | sof ROI")
    for uptime in (99.9, 98.0, 95.0, 80.0):
        f = Faraz(uptime_pct=uptime)
        gross, slash, net, roi = hisob(f)
        print(f"{uptime:6.1f}% | {gross:9.4f} | {slash:15.4f} | {net:7.4f} | {roi:6.2f}%")
    print("Izoh: haqiqiy validator rewards/penalties stake va tarmoq holatiga bog'liq.")
