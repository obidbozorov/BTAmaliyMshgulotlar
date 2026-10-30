// A14 · Token.sol (A13) uchun Hardhat testlari: fixture, revert, event, balans o'zgarishi
const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { expect } = require("chai");
const { ethers } = require("hardhat");

const PRC = (n) => ethers.parseUnits(String(n), 18);

describe("Token (ERC-20)", function () {
  // Fixture: har bir test toza holatdan boshlanadi, deploy esa bir marta bajarilib, snapshot'dan tiklanadi
  async function deployFixture() {
    const [egasi, ali, vali, dex] = await ethers.getSigners();
    const token = await ethers.deployContract("Token", [1000]);
    return { token, egasi, ali, vali, dex };
  }

  describe("Deploy", function () {
    it("nom, belgi va decimals to'g'ri", async function () {
      const { token } = await loadFixture(deployFixture);
      expect(await token.name()).to.equal("ProfiCoin");
      expect(await token.symbol()).to.equal("PRC");
      expect(await token.decimals()).to.equal(18n);
    });

    it("1000 PRC egasiga mint qilinadi", async function () {
      const { token, egasi } = await loadFixture(deployFixture);
      expect(await token.totalSupply()).to.equal(PRC(1000));
      expect(await token.balanceOf(egasi)).to.equal(PRC(1000));
    });
  });

  describe("transfer", function () {
    it("balanslarni o'zgartiradi va Transfer event chiqaradi", async function () {
      const { token, egasi, ali } = await loadFixture(deployFixture);
      const tx = token.transfer(ali, PRC(25));          // bitta tranzaksiyani ikki xil tekshiramiz
      await expect(tx).to.emit(token, "Transfer").withArgs(egasi.address, ali.address, PRC(25));
      await expect(tx).to.changeTokenBalances(token, [egasi, ali], [-PRC(25), PRC(25)]);
    });

    it("balans yetmasa rad etiladi", async function () {
      const { token, ali, vali } = await loadFixture(deployFixture);
      await expect(token.connect(ali).transfer(vali, 1n)).to.be.revertedWith("Balans yetarli emas");
    });

    it("0x0 manziliga yuborib bo'lmaydi", async function () {
      const { token } = await loadFixture(deployFixture);
      await expect(token.transfer(ethers.ZeroAddress, 1n)).to.be.revertedWith("Manzil bosh");
    });
  });

  describe("approve va transferFrom", function () {
    it("ruxsat doirasida o'tkazadi va allowance kamayadi", async function () {
      const { token, egasi, ali, dex } = await loadFixture(deployFixture);
      await expect(token.approve(dex, PRC(10))).to.emit(token, "Approval").withArgs(egasi.address, dex.address, PRC(10));
      await expect(token.connect(dex).transferFrom(egasi, ali, PRC(4)))
        .to.changeTokenBalances(token, [egasi, ali], [-PRC(4), PRC(4)]);
      expect(await token.allowance(egasi, dex)).to.equal(PRC(6));
    });

    it("ruxsatdan ortiq transferFrom rad etiladi", async function () {
      const { token, egasi, ali, dex } = await loadFixture(deployFixture);
      await token.approve(dex, PRC(1));
      await expect(token.connect(dex).transferFrom(egasi, ali, PRC(2))).to.be.revertedWith("Ruxsat yetarli emas");
    });

    it("cheksiz ruxsat kamaytirilmaydi", async function () {
      const { token, egasi, ali, dex } = await loadFixture(deployFixture);
      await token.approve(dex, ethers.MaxUint256);
      await token.connect(dex).transferFrom(egasi, ali, PRC(1));
      expect(await token.allowance(egasi, dex)).to.equal(ethers.MaxUint256);
    });
  });

  describe("mint va burn", function () {
    it("faqat egasi mint qila oladi", async function () {
      const { token, ali } = await loadFixture(deployFixture);
      await expect(token.connect(ali).mint(ali, 1n)).to.be.revertedWith("Faqat egasi");
    });

    it("burn totalSupply'ni kamaytiradi", async function () {
      const { token, egasi } = await loadFixture(deployFixture);
      await expect(token.burn(PRC(100)))
        .to.emit(token, "Transfer").withArgs(egasi.address, ethers.ZeroAddress, PRC(100));
      expect(await token.totalSupply()).to.equal(PRC(900));
    });
  });

  // Xossaga asoslangan test: tasodifiy o'tkazmalar ketma-ketligidan keyin ham invariant saqlanadi
  it("invariant: balanslar yig'indisi = totalSupply (50 ta tasodifiy o'tkazma)", async function () {
    const { token } = await loadFixture(deployFixture);
    const s = (await ethers.getSigners()).slice(0, 5);
    let urug = 2026n;                                         // takrorlanadigan psevdotasodifiy son
    const keyingi = () => (urug = (urug * 6364136223846793005n + 1442695040888963407n) % 2n ** 64n);
    for (let i = 0; i < 50; i++) {
      const kimdan = s[Number(keyingi() % 5n)], kimga = s[Number(keyingi() % 5n)];
      const balans = await token.balanceOf(kimdan);
      if (balans === 0n) continue;
      await token.connect(kimdan).transfer(kimga, keyingi() % (balans + 1n));
    }
    let yigindi = 0n;
    for (const a of s) yigindi += await token.balanceOf(a);
    expect(yigindi).to.equal(await token.totalSupply());
  });
});
