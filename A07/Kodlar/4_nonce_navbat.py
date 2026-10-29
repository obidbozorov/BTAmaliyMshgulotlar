# A7 · 4-skript: nonce navbati — nega bitta “tiqilgan” tx keyingilarini ham to'xtatadi?
def mempool(hisob_nonce, kelganlar):
    navbat, bajarildi = {}, []
    for n, izoh in kelganlar:
        if n < hisob_nonce:
            print(f"  nonce {n}: RAD — 'nonce too low' (allaqachon ishlatilgan)"); continue
        navbat[n] = izoh
        print(f"  nonce {n} keldi ({izoh})", end="")
        while hisob_nonce in navbat:                      # ketma-ket bo'lsa — blokka
            bajarildi.append((hisob_nonce, navbat.pop(hisob_nonce))); hisob_nonce += 1
        print(f" → bajarildi: {[b[0] for b in bajarildi]}, kutmoqda: {sorted(navbat)}")
    return hisob_nonce

if __name__ == "__main__":
    print("Hisobning joriy nonce'i = 5")
    yakun = mempool(5, [(7, "token sotish"), (6, "approve"), (4, "eski tx"), (5, "ETH o'tkazma"), (9, "NFT mint")])
    print("Yakuniy nonce:", yakun, "· nonce 9 — 8 kelmaguncha kutadi (bo'shliq)")
