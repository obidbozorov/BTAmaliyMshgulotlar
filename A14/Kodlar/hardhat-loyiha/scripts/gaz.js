// A14 · `npm run gaz` — testlarni gaz hisoboti bilan ishga tushiradi (Windows, macOS, Linux'da bir xil ishlaydi)
const { execSync } = require("child_process");
execSync("npx hardhat test", { stdio: "inherit", env: { ...process.env, REPORT_GAS: "true" } });
