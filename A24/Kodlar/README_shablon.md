# [Loyiha nomi] — blokcheynga asoslangan ilova prototipi

> A24 · Blokcheyn texnologiyalari · Yakuniy loyiha. Ushbu shablonni loyihangiz repozitoriyasining README.md fayli sifatida to'ldiring.

## 1. Jamoa

| A'zo | Roli | Asosiy hissasi (fayllar, commit'lar) |
|---|---|---|
| F.I.Sh. | Smart-kontrakt | `contracts/…` |
| F.I.Sh. | Frontend / integratsiya | `dapp/…` |
| F.I.Sh. | Test va audit | `test/…`, audit hisoboti |

## 2. Muammo va nega blokcheyn (TN8)

- **Muammo:** kim, qanday qiyinchilikka duch keladi?
- **Hozirgi yechim va uning kamchiligi:** markazlashgan tizim nima uchun yetarli emas?
- **Blokcheyn zarurligi testi** (har biriga “ha/yo'q” va izoh):
  1. Holatni (ma'lumotni) saqlash kerakmi?
  2. Yozuvchilar bir nechta va ular bir-biriga to'liq ishonmaydimi?
  3. Ishonchli uchinchi tomondan voz kechish istaladimi?
  4. Natijani tashqaridan har kim tekshira olishi kerakmi?
- **Tanlangan tarmoq va asos:** Sepolia / Base Sepolia / permissioned (A15, A10)

## 3. Arxitektura

```
Foydalanuvchi ─ MetaMask ─ DApp (dapp/) ─ RPC ─ Smart-kontrakt(lar)
                                   │                 ├─ Oracle (A17)?
                                   └─ IPFS (A16)?    └─ boshqa kontraktlar
```

| Komponent | Texnologiya | Manzil / havola |
|---|---|---|
| Kontrakt 1 | Solidity 0.8.x | 0x… (Sepolia, verify qilingan) |
| Frontend | HTML + ethers.js v6 | |
| Ma'lumot saqlash | on-chain / IPFS | |

**Zanjirda nima saqlanadi va nima saqlanmaydi?** (gaz, maxfiylik, shaxsiy ma'lumotlar)

## 4. Ishga tushirish

```bash
# Kontraktlar va testlar (A14)
cd hardhat-loyiha && npm install && npx hardhat test && npx hardhat coverage
# Frontend
cd dapp && python -m http.server 8000   # http://localhost:8000
```

## 5. Sifat va xavfsizlik (TN12)

- Testlar soni: __ · Qamrov (Stmts / Branch): __% / __%
- Slither natijasi: __ ta topilma, ulardan __ tasi tuzatildi, __ tasi asoslab qabul qilindi
- A23 chek-listi: reentrancy □ · ruxsat nazorati □ · tx.origin □ · unchecked □ · oracle tekshiruvi □ · tasodif □ · DoS □
- Asosiy amallar gazi (A15): deploy ____, asosiy funksiya ____ · L2 dagi taxminiy narx ____

## 6. Xavflar, boshqaruv va huquqiy masalalar (TN14)

- Kim admin huquqlariga ega? Kalit yo'qolsa yoki o'g'irlansa nima bo'ladi (multisig — A22)?
- Shaxsiy ma'lumotlar blokcheynga yozilmaydimi?
- O'zbekiston qonunchiligi: kripto-aktivlar aylanmasi (napp.uz, lex.uz) loyihaga qanday ta'sir qiladi?

## 7. Sun'iy intellektdan foydalanish (fan dasturi talabi)

| Vosita | Nima uchun ishlatildi | So'rov (prompt) | Natijaning qaysi qismi o'zgartirildi |
|---|---|---|---|
| | | | |

Jamoaning har bir a'zosi loyihadagi istalgan kodni og'zaki tushuntira olishi shart.

## 8. Demo

- Video (2–3 daqiqa) yoki jonli demo ssenariysi: 1) … 2) … 3) …
- Etherscan havolalari: kontrakt, demo tranzaksiyalari
