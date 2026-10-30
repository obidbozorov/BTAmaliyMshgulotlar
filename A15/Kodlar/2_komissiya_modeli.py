# A15 · 2-skript: bir xil amalning Ethereum (L1) va Base (L2) dagi narxini hisoblaydi
# Kiritma: 1_gaz_olchash.py yaratgan olchov.json. Narx parametrlari pastda — o'zgartirib tajriba qiling.
import json, sys
from l2_formula import l1_data_fee, bedrock_l1_data_fee

GWEI = 10**9
ETH_USD = 3000                       # SHARTLI kurs — hisob uchun
# 2026-10-29 dagi haqiqiy qiymatlar (3_jonli_tekshir.py bilan yangilang)
ETHEREUM = {"base_fee": 0.304 * GWEI, "tip": 0.05 * GWEI}
BASE = {"l2_base_fee": 0.005 * GWEI, "l2_tip": 0.001 * GWEI,
        "l1_base_fee": 417_747_611, "blob_base_fee": 23_283_785,          # GasPriceOracle qiymatlari (wei)
        "base_fee_scalar": 2269, "blob_base_fee_scalar": 1_055_762}

def hisobla(olchov, eth=ETHEREUM, base=BASE, blobsiz=False):
    natija = []
    for o in olchov:
        l1 = o["gaz"] * (eth["base_fee"] + eth["tip"])
        ijro = o["gaz"] * (base["l2_base_fee"] + base["l2_tip"])
        tx = bytes.fromhex(o["tx_hex"])
        data = (bedrock_l1_data_fee(tx, base["l1_base_fee"]) if blobsiz else
                l1_data_fee(tx, base["l1_base_fee"], base["blob_base_fee"], base["base_fee_scalar"], base["blob_base_fee_scalar"]))
        natija.append((o["amal"], l1, ijro, data))
    return natija

def jadval(natija, sarlavha):
    usd = lambda wei: f"${wei / 1e18 * ETH_USD:,.4f}"
    print(f"\n{sarlavha}  (1 ETH = ${ETH_USD:,} — shartli)")
    print(f"{'Amal':26}{'Ethereum L1':>13}{'Base: ijro':>13}{'Base: L1 data':>15}{'Base jami':>12}{'Arzonroq':>10}")
    for nom, l1, ijro, data in natija:
        print(f"{nom:26}{usd(l1):>13}{usd(ijro):>13}{usd(data):>15}{usd(ijro + data):>12}{l1 / (ijro + data):>9.0f}×")

if __name__ == "__main__":
    with open("olchov.json", encoding="utf-8") as f:
        olchov = json.load(f)
    jadval(hisobla(olchov), "1) Bugungi narxlar")
    band = {"base_fee": 30 * GWEI, "tip": 2 * GWEI}                # tarmoq band bo'lgan kun (2021–2024 dagi odatiy holat)
    jadval(hisobla(olchov, band, {**BASE, "l1_base_fee": 30 * GWEI}), "2) L1 band: baseFee = 30 gwei")
    jadval(hisobla(olchov, band, {**BASE, "l1_base_fee": 30 * GWEI}, blobsiz=True),
           "3) 2023-yil: blob yo'q (Bedrock formulasi), L1 baseFee = 30 gwei")
