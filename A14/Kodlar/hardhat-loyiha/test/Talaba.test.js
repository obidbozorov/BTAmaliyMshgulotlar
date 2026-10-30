// A14 · TALABA TOPSHIRIG'I: uchta testni o'zingiz yozing.
// Har birida "it.skip" ni "it" ga almashtiring, TODO ni to'ldiring va `npx hardhat test` bilan tekshiring.
const { loadFixture, time } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Talaba testlari", function () {
  async function fixture() {
    const [egasi, ali] = await ethers.getSigners();
    const token = await ethers.deployContract("Token", [1000]);
    const yigim = await ethers.deployContract("Yigim", [ethers.parseEther("5"), 7 * 24 * 60 * 60]);
    return { token, yigim, egasi, ali };
  }

  it.skip("T1: 0 ETH bilan hissaQosh rad etiladi (\"Summa nol\")", async function () {
    const { yigim, ali } = await loadFixture(fixture);
    // TODO: revertedWith dan foydalaning
  });

  it.skip("T2: maqsadga yetilgan bo'lsa qaytar() MaqsadgaYetilgan xatosini beradi", async function () {
    const { yigim, ali } = await loadFixture(fixture);
    // TODO: 5 ETH hissa qo'shing, vaqtni muddatdan o'tkazing, revertedWithCustomError bilan tekshiring
  });

  it.skip("T3: mint totalSupply'ni oshiradi va Transfer(0x0 → ali) event chiqaradi", async function () {
    const { token, ali } = await loadFixture(fixture);
    // TODO: emit(...).withArgs(ethers.ZeroAddress, ali.address, ...) va totalSupply tekshiruvi
  });
});
