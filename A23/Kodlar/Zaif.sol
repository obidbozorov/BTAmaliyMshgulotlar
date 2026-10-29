// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// A23 · AUDIT UCHUN ATAYLAB ZAIF YOZILGAN KONTRAKTLAR. Hech qachon real tarmoqda ishlatmang!
// Har bir kontraktda bitta zaiflik bor. Vazifa: topish, hujum bilan isbotlash, tuzatish.

/// 1) Bank: foydalanuvchilar ETH qo'yadi va qaytarib oladi
contract ZaifBank {
    mapping(address => uint256) public balans;

    function qoy() external payable {
        balans[msg.sender] += msg.value;
    }

    function ol() external {
        uint256 s = balans[msg.sender];
        require(s > 0, "Balans yoq");
        (bool ok, ) = msg.sender.call{value: s}("");
        require(ok, "Otkazma xato");
        balans[msg.sender] = 0;
    }
}

/// 2) Shaxsiy hamyon: faqat egasi pul yubora oladi
contract ZaifHamyon {
    address public egasi;

    constructor() payable { egasi = msg.sender; }

    function yubor(address payable kimga, uint256 summa) external {
        require(tx.origin == egasi, "Faqat egasi");
        kimga.transfer(summa);
    }

    receive() external payable {}
}

/// 3) Mukofot tokeni: egasi talabalar uchun ball (token) chiqaradi
contract ZaifToken {
    address public egasi;
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    constructor() { egasi = msg.sender; }

    function mint(address kimga, uint256 summa) external {
        balanceOf[kimga] += summa;
        totalSupply += summa;
    }

    function transfer(address kimga, uint256 summa) external {
        require(balanceOf[msg.sender] >= summa, "Balans yetarli emas");
        balanceOf[msg.sender] -= summa;
        balanceOf[kimga] += summa;
    }
}

/// 4) Ommaviy to'lov: bitta tranzaksiyada ko'p oluvchiga bir xil summa (gazni tejash uchun unchecked)
contract ZaifOmmaviy {
    mapping(address => uint256) public balanceOf;

    constructor() { balanceOf[msg.sender] = 1000 ether; }

    function ommaviyOtkaz(address[] calldata oluvchilar, uint256 qiymat) external {
        uint256 jami;
        unchecked { jami = oluvchilar.length * qiymat; }
        require(balanceOf[msg.sender] >= jami, "Balans yetarli emas");
        balanceOf[msg.sender] -= jami;
        for (uint256 i = 0; i < oluvchilar.length; i++) {
            balanceOf[oluvchilar[i]] += qiymat;
        }
    }
}

/// 5) Lotereya: 0,1 ETH tikiladi, “tasodifiy” son 0 chiqsa — butun kassa yutuq
contract ZaifLotereya {
    constructor() payable {}

    function oyna(uint256 taxmin) external payable {
        require(msg.value == 0.1 ether, "0.1 ETH tiking");
        uint256 son = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, msg.sender))) % 10;
        if (son == taxmin) {
            (bool ok, ) = msg.sender.call{value: address(this).balance}("");
            require(ok, "Otkazma xato");
        }
    }
}

/// 6) Auksion: eng yuqori taklif yutadi, oldingi yetakchiga puli darhol qaytariladi
contract ZaifAuksion {
    address public yetakchi;
    uint256 public engYuqori;

    function taklif() external payable {
        require(msg.value > engYuqori, "Taklif past");
        if (yetakchi != address(0)) {
            (bool ok, ) = yetakchi.call{value: engYuqori}("");
            require(ok, "Qaytarish xato");
        }
        yetakchi = msg.sender;
        engYuqori = msg.value;
    }
}
