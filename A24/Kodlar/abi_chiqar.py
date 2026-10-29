# A24 · Kontraktdan ABI ni chiqaradi: dapp/config.js uchun “human-readable” ro'yxat va to'liq abi.json
# Ishga tushirish: python abi_chiqar.py <Fayl.sol> <KontraktNomi>     masalan: python abi_chiqar.py ../../A13/Kodlar/Token.sol Token
import json, sys, solcx

if len(sys.argv) < 3:
    sys.exit("Foydalanish: python abi_chiqar.py <Fayl.sol> <KontraktNomi>")
fayl, nom = sys.argv[1], sys.argv[2]
solcx.install_solc("0.8.28")
natija = solcx.compile_files([fayl], output_values=["abi"], solc_version="0.8.28")
kalit = next((k for k in natija if k.endswith(":" + nom)), None)       # solc fayl yo'lini o'zicha yozishi mumkin
if not kalit:
    sys.exit(f"{nom} kontrakti topilmadi. Mavjudlari: {[k.split(':')[-1] for k in natija]}")
abi = natija[kalit]["abi"]

def tur(p):
    if p["type"].startswith("tuple"):
        return "(" + ",".join(tur(c) for c in p["components"]) + ")" + p["type"][5:]
    return p["type"]

def qator(e):
    args = ", ".join(tur(p) + (" indexed" if p.get("indexed") else "") + (" " + p["name"] if p.get("name") else "") for p in e.get("inputs", []))
    if e["type"] == "event":
        return f"event {e['name']}({args})"
    if e["type"] == "error":
        return f"error {e['name']}({args})"
    if e["type"] != "function":
        return None
    holat = " view" if e["stateMutability"] == "view" else " pure" if e["stateMutability"] == "pure" else " payable" if e["stateMutability"] == "payable" else ""
    natija = ", ".join(tur(p) for p in e.get("outputs", []))
    return f"function {e['name']}({args}){holat}" + (f" returns ({natija})" if natija else "")

with open("abi.json", "w", encoding="utf-8") as f:
    json.dump(abi, f, indent=2)
print("// config.js dagi ABI: [ … ] o'rniga qo'ying")
print("ABI: [\n" + "\n".join(f"  {json.dumps(q, ensure_ascii=False)}," for q in map(qator, abi) if q) + "\n],")
print(f"\nTo'liq ABI saqlandi: abi.json ({len(abi)} element)")
