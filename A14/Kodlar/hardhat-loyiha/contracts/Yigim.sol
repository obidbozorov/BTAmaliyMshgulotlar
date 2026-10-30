// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Yigim — A14: muddatli kraudfanding (vaqt, ETH va custom error'larni testlash uchun)
/// Maqsadga muddat ichida yetilsa — egasi pulni oladi, yetilmasa — har kim o'z hissasini qaytaradi.
contract Yigim {
    address public immutable egasi;
    uint256 public immutable maqsad;     // wei
    uint256 public immutable muddat;     // unix vaqt
    uint256 public jami;
    bool public olindi;
    mapping(address => uint256) public hissa;

    error FaqatEgasi();
    error MuddatTugagan();
    error MuddatTugamagan();
    error MaqsadgaYetilmadi(uint256 jami, uint256 maqsad);
    error MaqsadgaYetilgan();
    error HissaYoq();

    event HissaQoshildi(address indexed kim, uint256 summa);
    event Olindi(uint256 summa);
    event Qaytarildi(address indexed kim, uint256 summa);

    constructor(uint256 _maqsad, uint256 davomiylik) {
        require(_maqsad > 0, "Maqsad nol");
        egasi = msg.sender;
        maqsad = _maqsad;
        muddat = block.timestamp + davomiylik;
    }

    function hissaQosh() external payable {
        if (block.timestamp >= muddat) revert MuddatTugagan();
        require(msg.value > 0, "Summa nol");
        hissa[msg.sender] += msg.value;
        jami += msg.value;
        emit HissaQoshildi(msg.sender, msg.value);
    }

    function ol() external {
        if (msg.sender != egasi) revert FaqatEgasi();
        if (block.timestamp < muddat) revert MuddatTugamagan();
        if (jami < maqsad) revert MaqsadgaYetilmadi(jami, maqsad);
        require(!olindi, "Allaqachon olingan");
        olindi = true;
        emit Olindi(jami);
        (bool ok, ) = egasi.call{value: jami}("");
        require(ok, "Otkazma xato");
    }

    function qaytar() external {
        if (block.timestamp < muddat) revert MuddatTugamagan();
        if (jami >= maqsad) revert MaqsadgaYetilgan();
        uint256 s = hissa[msg.sender];
        if (s == 0) revert HissaYoq();
        hissa[msg.sender] = 0;                       // avval holat,
        emit Qaytarildi(msg.sender, s);
        (bool ok, ) = msg.sender.call{value: s}(""); // keyin o'tkazma (A12, 12.4)
        require(ok, "Otkazma xato");
    }
}
