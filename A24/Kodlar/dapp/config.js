// A24 · DApp sozlamalari — o'z loyihangiz kontrakti va tarmog'i bilan almashtiring
window.DAPP_CONFIG = {
  // A13 da Sepolia'ga deploy qilgan tokeningiz manzili
  KONTRAKT: "0x0000000000000000000000000000000000000000",
  TARMOQ: {
    chainId: 11155111,                          // Sepolia
    nomi: "Sepolia",
    explorer: "https://sepolia.etherscan.io",
  },
  // ABI ning faqat kerakli qismi (ethers.js “human-readable” formati).
  // To'liq ABI ni Remix → Compiler → ABI yoki abi_chiqar.py orqali olish mumkin.
  ABI: [
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function decimals() view returns (uint8)",
    "function totalSupply() view returns (uint256)",
    "function balanceOf(address) view returns (uint256)",
    "function transfer(address to, uint256 value) returns (bool)",
    "event Transfer(address indexed from, address indexed to, uint256 value)",
  ],
};
