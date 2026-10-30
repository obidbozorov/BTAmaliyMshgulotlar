// A14 · Yigim.sol testlari: vaqtni boshqarish (time), ETH balansi va custom error'lar
const { loadFixture, time } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { expect } = require("chai");
const { ethers } = require("hardhat");

const ETH = (n) => ethers.parseEther(String(n));
const KUN = 24 * 60 * 60;

describe("Yigim (kraudfanding)", function () {
  async function deployFixture() {
    const [egasi, ali, vali] = await ethers.getSigners();
    const yigim = await ethers.deployContract("Yigim", [ETH(5), 7 * KUN]);   // maqsad 5 ETH, 7 kun
    return { yigim, egasi, ali, vali };
  }

  it("hissa qo'shiladi va ETH kontraktga o'tadi", async function () {
    const { yigim, ali } = await loadFixture(deployFixture);
    const tx = yigim.connect(ali).hissaQosh({ value: ETH(2) });
    await expect(tx).to.emit(yigim, "HissaQoshildi").withArgs(ali.address, ETH(2));
    await expect(tx).to.changeEtherBalances([ali, yigim], [-ETH(2), ETH(2)]);
    expect(await yigim.jami()).to.equal(ETH(2));
  });

  it("muddat tugagach hissa qabul qilinmaydi (custom error)", async function () {
    const { yigim, ali } = await loadFixture(deployFixture);
    await time.increase(7 * KUN);                                  // 7 kun oldinga "sakraymiz"
    await expect(yigim.connect(ali).hissaQosh({ value: ETH(1) })).to.be.revertedWithCustomError(yigim, "MuddatTugagan");
  });

  it("muddat tugamasdan egasi pulni ololmaydi", async function () {
    const { yigim, ali } = await loadFixture(deployFixture);
    await yigim.connect(ali).hissaQosh({ value: ETH(6) });
    await expect(yigim.ol()).to.be.revertedWithCustomError(yigim, "MuddatTugamagan");
  });

  it("maqsadga yetilsa, muddatdan keyin egasi oladi", async function () {
    const { yigim, egasi, ali, vali } = await loadFixture(deployFixture);
    await yigim.connect(ali).hissaQosh({ value: ETH(3) });
    await yigim.connect(vali).hissaQosh({ value: ETH(2) });
    await time.increaseTo(await yigim.muddat());
    await expect(yigim.ol()).to.changeEtherBalances([egasi, yigim], [ETH(5), -ETH(5)]);
    await expect(yigim.ol()).to.be.revertedWith("Allaqachon olingan");
  });

  it("begona ol() ni chaqira olmaydi", async function () {
    const { yigim, ali } = await loadFixture(deployFixture);
    await time.increase(8 * KUN);
    await expect(yigim.connect(ali).ol()).to.be.revertedWithCustomError(yigim, "FaqatEgasi");
  });

  it("maqsadga yetilmasa: egasi ololmaydi, hissadorlar qaytarib oladi", async function () {
    const { yigim, ali } = await loadFixture(deployFixture);
    await yigim.connect(ali).hissaQosh({ value: ETH(1) });
    await time.increase(8 * KUN);
    await expect(yigim.ol()).to.be.revertedWithCustomError(yigim, "MaqsadgaYetilmadi").withArgs(ETH(1), ETH(5));
    await expect(yigim.connect(ali).qaytar()).to.changeEtherBalances([ali, yigim], [ETH(1), -ETH(1)]);
    await expect(yigim.connect(ali).qaytar()).to.be.revertedWithCustomError(yigim, "HissaYoq");
  });
});
