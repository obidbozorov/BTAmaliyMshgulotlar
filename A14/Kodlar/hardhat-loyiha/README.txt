A14 · Hardhat loyihasi — smart-kontraktlarni avtomatik testlash

Talab: Node.js 18 yoki yangiroq (nodejs.org, LTS versiya).

O'rnatish (bir marta, internet kerak):  npm install
Kompilyatsiya:                          npx hardhat compile
Testlar:                                npx hardhat test
Bitta fayl:                             npx hardhat test test/Talaba.test.js
Gaz hisoboti:                           npm run gaz
Qamrov (coverage):                      npx hardhat coverage   -> coverage/index.html

Tuzilma:
  contracts/Token.sol      — A13 dagi ERC-20 token
  contracts/Yigim.sol      — muddatli kraudfanding (vaqt va ETH testlari uchun)
  test/Token.test.js       — 11 ta tayyor test (fixture, revert, event, invariant)
  test/Yigim.test.js       — 6 ta tayyor test (time.increase, custom error)
  test/Talaba.test.js      — talaba yozadigan 3 ta test (it.skip -> it)

node_modules, artifacts, cache, coverage papkalarini topshiriqqa qo'shmang.
