# A11 · ixtiyoriy: Hisob.sol ni mahalliy EVM'da sinash (Remix'dagi qo'lda sinovning avtomatik nusxasi)
# O'rnatish: pip install "web3[tester]" py-solc-x   ·   ishga tushirish: python test_hisob.py
import solcx
from web3 import Web3, EthereumTesterProvider
solcx.install_solc("0.8.28")
out = solcx.compile_files(["Hisob.sol"], output_values=["abi", "bin"], solc_version="0.8.28")
abi, bin_ = out["Hisob.sol:Hisob"]["abi"], out["Hisob.sol:Hisob"]["bin"]
w3 = Web3(EthereumTesterProvider()); egasi, ali, vali = w3.eth.accounts[:3]
r = w3.eth.wait_for_transaction_receipt(w3.eth.contract(abi=abi, bytecode=bin_).constructor().transact({"from": egasi}))
h = w3.eth.contract(address=r.contractAddress, abi=abi)
print("Deploy gazi:", r.gasUsed, "| egasi to'g'rimi:", h.functions.egasi().call() == egasi)
r = w3.eth.wait_for_transaction_receipt(h.functions.tolash(ali, 100).transact({"from": egasi}))
ev = h.events.Tolov().process_receipt(r)[0]["args"]
print("tolash(ali,100) gazi:", r.gasUsed, "| event:", dict(ev))
print("Ali qoldig'i:", h.functions.meningQoldigim().call({"from": ali}), "| jami:", h.functions.jami().call())
try:
    h.functions.tolash(vali, 5).call({"from": ali}); print("XATO: begona to'lay oldi!")
except Exception as e:
    print("Ali to'lashga urindi → rad etildi:", "Faqat egasi" in str(e))
try:
    h.functions.tolash(ali, 0).call({"from": egasi})
except Exception as e:
    print("Nol summa → rad etildi:", "Summa nol" in str(e))
