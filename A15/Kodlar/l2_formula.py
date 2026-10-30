# A15 · OP Stack (Base, Optimism) L1 ma'lumot komissiyasi — Fjord formulasi
# Manba: Optimism specs, "Fjord: L1 cost" va GasPriceOracle (0x4200…000F) kontrakti.
# FastLZ siqish — solady LibZip.flzCompress ning Python nusxasi (kontrakt aynan shuni ishlatadi).

COST_INTERCEPT = -42_585_600      # chiziqli regressiya koeffitsientlari (1e6 masshtabda)
COST_FASTLZ_COEF = 836_500
MIN_TX_SIZE = 100                 # bayt
IMZO_QOSHIMCHA = 68               # imzo va RLP qo'shimchasi uchun qo'shiladigan baytlar


def flz_uzunlik(data: bytes) -> int:
    """FastLZ (1-daraja) bilan siqilgan ma'lumot uzunligi, baytda."""
    ib, n = data, len(data)
    b = n - 4
    ht = {}
    o = 0          # chiqish uzunligi (faqat uzunlik kerak)
    a, i = 0, 2

    def u24(k): return ib[k] | (ib[k + 1] << 8) | (ib[k + 2] << 16)
    def h(x): return ((2654435769 * x) >> 19) & 8191

    def literallar(r):
        nonlocal o
        while r >= 32:
            o += 33; r -= 32
        if r:
            o += r + 1

    while i < b - 9:
        while True:
            s = u24(i); hh = h(s)
            r = ht.get(hh, 0); ht[hh] = i
            d = i - r
            c = u24(r) if d < 8192 else 0x1000000
            if i >= b - 9:
                break
            i += 1
            if s == c:
                break
        if i >= b - 9:
            break
        i -= 1
        if i > a:
            literallar(i - a)
        l, p, q = 0, r + 3, i + 3
        e = b - q
        while l < e:                      # birinchi mos kelmagan bayt ham hisobga qo'shiladi (FastLZ qoidasi)
            teng = ib[p + l] == ib[q + l]
            l += 1
            if not teng:
                break
        i += l
        d -= 1
        while l > 262:
            o += 3; l -= 262
        o += 2 if l < 7 else 3
        ht[h(u24(i))] = i; i += 1
        ht[h(u24(i))] = i; i += 1
        a = i
    literallar(b + 4 - a)
    return o


def l1_data_fee(tx_bayt: bytes, l1_base_fee, blob_base_fee, base_fee_scalar, blob_base_fee_scalar) -> int:
    """L2 tranzaksiyasi uchun L1'ga ma'lumot yozish narxi (wei). tx_bayt — imzosiz RLP tranzaksiya."""
    fastlz = flz_uzunlik(tx_bayt) + IMZO_QOSHIMCHA
    hajm = max(COST_INTERCEPT + COST_FASTLZ_COEF * fastlz, MIN_TX_SIZE * 10**6)
    narx = base_fee_scalar * 16 * l1_base_fee + blob_base_fee_scalar * blob_base_fee
    return hajm * narx // 10**12


def imzosiz_1559(chain_id, nonce, tip, max_fee, gas, to, value, data: bytes) -> bytes:
    """EIP-1559 (0x02) tranzaksiyasining imzosiz RLP ko'rinishi — GasPriceOracle.getL1Fee shuni kutadi."""
    import rlp
    to_b = bytes.fromhex(to[2:]) if to else b""
    return b"\x02" + rlp.encode([chain_id, nonce, tip, max_fee, gas, to_b, value, data, []])


def bedrock_l1_data_fee(tx_bayt: bytes, l1_base_fee, overhead=188, scalar=0.684) -> int:
    """EIP-4844 (blob) dan oldingi Bedrock formulasi: L1 calldata gazi × L1 baseFee × skalar.
    Imzo uchun 68 ta nol bo'lmagan bayt qo'shiladi. Base 2023-yilda overhead=188, scalar=0.684 ishlatgan."""
    gaz = sum(4 if x == 0 else 16 for x in tx_bayt) + 68 * 16 + overhead
    return int(gaz * l1_base_fee * scalar)
