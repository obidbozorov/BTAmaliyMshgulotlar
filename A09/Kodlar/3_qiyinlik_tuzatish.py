# A9 · 3-skript: Bitcoin qiyinligini qayta hisoblash (har 2016 blokda)
# yangi = eski × (kutilgan vaqt / haqiqiy vaqt), o'zgarish 4 barobardan oshmaydi
KUTILGAN = 2016 * 600                                  # 2 hafta, sekundda

def tuzat(qiyinlik, haqiqiy_vaqt):
    haqiqiy = min(max(haqiqiy_vaqt, KUTILGAN / 4), KUTILGAN * 4)
    return qiyinlik * KUTILGAN / haqiqiy

if __name__ == "__main__":
    qiyinlik, xeshreyt = 1.0, 1.0                     # nisbiy birliklar
    print(f"{'Davr':>5}{'Xeshreyt':>10}{'Blok vaqti, daq':>17}{'Yangi qiyinlik':>16}")
    for davr, x in enumerate([1, 1, 2, 2, 2, 0.5, 0.5, 10, 10, 10], 1):
        blok_vaqti = 600 * qiyinlik / x               # o'rtacha blok vaqti
        qiyinlik = tuzat(qiyinlik, blok_vaqti * 2016)
        print(f"{davr:>5}{x:>10}{blok_vaqti/60:>17.1f}{qiyinlik:>16.2f}")
