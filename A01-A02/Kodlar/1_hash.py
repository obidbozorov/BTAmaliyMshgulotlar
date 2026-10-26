# 1-topshiriq: SHA-256 xeshini hisoblash
import hashlib

matn = input("Matnni kiriting: ")
xesh = hashlib.sha256(matn.encode("utf-8")).hexdigest()

print("Matn      :", matn)
print("SHA-256   :", xesh)
print("Uzunligi  :", len(xesh), "belgi =", len(xesh) * 4, "bit")
