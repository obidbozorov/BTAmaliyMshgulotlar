# A16 · 2-skript: IPFS'dagi fayl CID ga mos kelishini tekshiradi (gateway'ga ishonmaslik — A8 g'oyasi)
# Foydalanish: python 2_cid_tekshir.py <fayl>            — faylning CID ini hisoblaydi
#              python 2_cid_tekshir.py <bafkrei… CID>   — gateway'dan yuklab, xeshini tekshiradi
import sys, os, hashlib, urllib.request
from cid import cid_v1, cid_dan_xesh

GATEWAY = ["https://ipfs.io/ipfs/", "https://dweb.link/ipfs/", "https://gateway.pinata.cloud/ipfs/", "https://w3s.link/ipfs/"]
if len(sys.argv) < 2:
    sys.exit(__doc__ or "Foydalanish: python 2_cid_tekshir.py <fayl | CID>")
arg = sys.argv[1].removeprefix("ipfs://")
if os.path.isfile(arg):
    with open(arg, "rb") as f: print(f"{arg} → {cid_v1(f.read())}")
    sys.exit()
kutilgan = cid_dan_xesh(arg)
for g in GATEWAY:
    try:
        with urllib.request.urlopen(urllib.request.Request(g + arg, headers={"User-Agent": "A16"}), timeout=20) as r:
            mazmun = r.read()
    except Exception as e:
        print(f"{g:38} — olinmadi ({type(e).__name__})"); continue
    ok = hashlib.sha256(mazmun).digest() == kutilgan
    print(f"{g:38} — {len(mazmun)} bayt, CID ga mos: {ok}")
    if ok:
        print(mazmun[:300].decode("utf-8", "replace")); break
