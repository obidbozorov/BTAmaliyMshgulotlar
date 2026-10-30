// A14 · Hardhat sozlamalari
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.28",
  gasReporter: {
    enabled: process.env.REPORT_GAS === "true",   // npm run gaz
    currency: "USD",
    outputFile: process.env.GAS_FAYL,              // ixtiyoriy: hisobot faylga
    noColors: !!process.env.GAS_FAYL,
  },
};
