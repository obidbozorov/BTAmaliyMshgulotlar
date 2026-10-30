# A7 · 3-skript: komissiya qayerga ketadi? (EIP-1559: yoqiladigan qism + choy puli)
GWEI = 10**9

def hisobla(gaz, base, tip, max_fee):
    if max_fee < base:
        return None                                  # tx blokka kira olmaydi — kutadi
    samarali = min(max_fee, base + tip)              # haqiqiy to'lanadigan narx
    return {"to'landi": gaz * samarali, "yoqildi": gaz * base,
            "validatorga": gaz * (samarali - base), "ortiqcha (olinmadi)": gaz * (max_fee - samarali)}

if __name__ == "__main__":
    gaz, tip, max_fee = 21000, 1.5 * GWEI, 30 * GWEI
    for base_gwei in [0.5, 10, 29, 35]:
        r = hisobla(gaz, base_gwei * GWEI, tip, max_fee)
        print(f"\nbaseFee = {base_gwei} gwei:")
        if r is None:
            print("  maxFee < baseFee → tranzaksiya mempool'da kutib turadi"); continue
        for k, v in r.items(): print(f"  {k:24} {v/1e18:.8f} ETH")
