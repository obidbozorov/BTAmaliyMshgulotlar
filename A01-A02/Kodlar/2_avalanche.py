# 2-topshiriq: Avalanche effektini o'lchash
import hashlib

def xesh(matn):
    return hashlib.sha256(matn.encode("utf-8")).hexdigest()

def bitlarga(hex_satr):
    """O'n oltilik satrni bitlar satriga aylantiradi"""
    return bin(int(hex_satr, 16))[2:].zfill(256)

a = input("Birinchi matn : ")
b = input("Ikkinchi matn : ")

xa, xb = xesh(a), xesh(b)
ba, bb = bitlarga(xa), bitlarga(xb)

farq = sum(1 for i in range(256) if ba[i] != bb[i])

print("\n1-xesh :", xa)
print("2-xesh :", xb)
print(f"\nFarq qilgan bitlar soni : {farq} / 256")
print(f"Foizda                  : {farq / 256 * 100:.1f}%")
