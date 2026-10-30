# A17 · 1-skript: Chainlink narx manbalarini tarmoqdan o'qiydi (faqat o'qish — hamyon kerak emas)
# Ishga tushirish: python 1_narx_oqish.py [--mainnet]
import sys, time, datetime
from web3 import Web3

ABI = [{"name": "latestRoundData", "type": "function", "stateMutability": "view", "inputs": [], "outputs": [
           {"name": "roundId", "type": "uint80"}, {"name": "answer", "type": "int256"}, {"name": "startedAt", "type": "uint256"},
           {"name": "updatedAt", "type": "uint256"}, {"name": "answeredInRound", "type": "uint80"}]},
       {"name": "getRoundData", "type": "function", "stateMutability": "view", "inputs": [{"name": "_roundId", "type": "uint80"}], "outputs": [
           {"name": "roundId", "type": "uint80"}, {"name": "answer", "type": "int256"}, {"name": "startedAt", "type": "uint256"},
           {"name": "updatedAt", "type": "uint256"}, {"name": "answeredInRound", "type": "uint80"}]},
       {"name": "decimals", "type": "function", "stateMutability": "view", "inputs": [], "outputs": [{"type": "uint8"}]},
       {"name": "description", "type": "function", "stateMutability": "view", "inputs": [], "outputs": [{"type": "string"}]}]

if "--mainnet" in sys.argv:
    RPC, MANBALAR = "https://ethereum-rpc.publicnode.com", {"ETH/USD": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"}
else:   # Sepolia manzillari: docs.chain.link/data-feeds/price-feeds/addresses
    RPC = "https://ethereum-sepolia-rpc.publicnode.com"
    MANBALAR = {"ETH/USD": "0x694AA1769357215DE4FAC081bf1f309aDC325306", "BTC/USD": "0x1b44F3514812d835EB1BDB0acB33d3fA3351Ee43"}

w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs={"timeout": 20}))
vaqt = lambda t: datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
for nom, manzil in MANBALAR.items():
    c = w3.eth.contract(address=manzil, abi=ABI)
    d = c.functions.decimals().call()
    rid, javob, _, yangilangan, _ = c.functions.latestRoundData().call()
    faza, raund = rid >> 64, rid & (2**64 - 1)          # roundId = (phaseId << 64) | aggregatorRoundId
    print(f"\n{c.functions.description().call()}  ({manzil})")
    print(f"  Narx: {javob / 10**d:,.2f} USD   decimals = {d}   xom javob = {javob}")
    print(f"  Yangilangan: {vaqt(yangilangan)} — {(time.time() - yangilangan) / 60:.0f} daqiqa oldin")
    print(f"  roundId = {rid}  →  phaseId {faza}, raund {raund}")
    print("  Oldingi raundlar:")
    oldingi = None
    for k in range(5, -1, -1):
        _, j, _, t, _ = c.functions.getRoundData((faza << 64) | (raund - k)).call()
        ozg = f"{(j - oldingi) / oldingi:+.3%}" if oldingi else ""
        interval = f"{(t - oldingi_t) / 60:5.0f} daq" if oldingi else ""
        print(f"    raund {raund - k}: {j / 10**d:>12,.2f}  {vaqt(t)}  {interval:>9} {ozg:>9}")
        oldingi, oldingi_t = j, t
