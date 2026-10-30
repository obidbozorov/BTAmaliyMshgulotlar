# A16 · 1-skript: har bir talaba uchun sertifikat rasmi (SVG) va metama'lumot (JSON) yaratadi, CID larini hisoblaydi
# Ishga tushirish: python 1_metadata.py [sertifikatlar.csv]   → chiqish/ papkasi
import csv, json, os, sys, html
from cid import cid_v1

KIRISH = sys.argv[1] if len(sys.argv) > 1 else "sertifikatlar.csv"
os.makedirs("chiqish", exist_ok=True)

def svg(ism, kurs, mavzu, ball, n):
    e = lambda s: html.escape(str(s))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
<rect width="600" height="400" fill="#F1EEFC"/><rect x="12" y="12" width="576" height="376" fill="none" stroke="#3B2FA8" stroke-width="4"/>
<text x="300" y="70" font-family="Times New Roman" font-size="22" text-anchor="middle" fill="#5F5A7A">PROFI UNIVERSITY · UniChain</text>
<text x="300" y="130" font-family="Times New Roman" font-size="40" font-weight="bold" text-anchor="middle" fill="#3B2FA8">SERTIFIKAT № {n}</text>
<text x="300" y="200" font-family="Times New Roman" font-size="30" text-anchor="middle" fill="#1D1B3A">{e(ism)}</text>
<text x="300" y="250" font-family="Times New Roman" font-size="20" text-anchor="middle" fill="#1D1B3A">{e(mavzu)} · {e(kurs)}-kurs</text>
<text x="300" y="300" font-family="Times New Roman" font-size="24" text-anchor="middle" fill="#3B2FA8">Ball: {e(ball)} / 100</text>
</svg>
""".encode("utf-8")

royxat = []
with open(KIRISH, encoding="utf-8") as f:
    for n, q in enumerate(csv.DictReader(f), 1):
        rasm = svg(q["ism"], q["kurs"], q["mavzu"], q["ball"], n)
        rasm_cid = cid_v1(rasm)
        with open(f"chiqish/{n}.svg", "wb") as g: g.write(rasm)
        # OpenSea va hamyonlar tushunadigan metama'lumot standarti
        meta = {"name": f"UniChain Sertifikat #{n}",
                "description": f"{q['ism']} — {q['mavzu']} fanini muvaffaqiyatli tamomlagani haqida sertifikat.",
                "image": f"ipfs://{rasm_cid}",
                "attributes": [{"trait_type": "Kurs", "value": int(q["kurs"])},
                               {"trait_type": "Ball", "value": int(q["ball"])},
                               {"trait_type": "Fan", "value": q["mavzu"]}]}
        meta_bayt = (json.dumps(meta, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        meta_cid = cid_v1(meta_bayt)
        with open(f"chiqish/{n}.json", "wb") as g: g.write(meta_bayt)
        royxat.append((n, q["ism"], rasm_cid, meta_cid))
        print(f"#{n} {q['ism']:18} rasm: {rasm_cid}\n   {'':18} meta: {meta_cid}  → tokenURI = ipfs://{meta_cid}")

with open("chiqish/mint_royxati.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["tokenId", "ism", "rasm_cid", "tokenURI"])
    for n, ism, r, m in royxat: w.writerow([n, ism, r, f"ipfs://{m}"])
print("\nSaqlandi: chiqish/*.svg, chiqish/*.json, chiqish/mint_royxati.csv")
print("Avval .svg fayllarni, keyin .json fayllarni IPFS'ga yuklang — CID lar yuqoridagi bilan bir xil chiqishi kerak.")
