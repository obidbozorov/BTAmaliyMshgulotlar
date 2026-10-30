-- A19 · 2-fayl: beshta asosiy so'rov. DuckDB'da ham, Dune'da ham ishlaydi.
-- Dune'da jadval nomi: ethereum.transactions (mashq bazasida: ethereum_transactions)

-- [1] Kunlik tranzaksiyalar soni
SELECT date_trunc('day', block_time) AS kun, count(*) AS tx_soni
FROM ethereum_transactions
GROUP BY 1 ORDER BY 1;

-- [2] Kunlik komissiya (ETH): gas_used × gas_price / 10^18
SELECT date_trunc('day', block_time) AS kun,
       round(sum(gas_used * gas_price) / 1e18, 4) AS komissiya_eth
FROM ethereum_transactions
GROUP BY 1 ORDER BY 1;

-- [3] Eng faol 10 ta yuboruvchi
SELECT "from" AS manzil, count(*) AS tx_soni, round(sum(value) / 1e18, 2) AS yuborilgan_eth
FROM ethereum_transactions
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;

-- [4] Muvaffaqiyatsiz tranzaksiyalar ulushi
SELECT round(100.0 * sum(CASE WHEN success THEN 0 ELSE 1 END) / count(*), 2) AS xato_foiz
FROM ethereum_transactions;

-- [5] Haftalik gaz narxi medianasi (gwei)
-- Dune'da: approx_percentile(gas_price, 0.5)   |   DuckDB'da: median(gas_price)
SELECT date_trunc('week', block_time) AS hafta,
       round(median(gas_price) / 1e9, 3) AS median_gwei
FROM ethereum_transactions
GROUP BY 1 ORDER BY 1;
