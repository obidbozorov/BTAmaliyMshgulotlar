// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Hisob — A11: birinchi smart-kontrakt (M7 ma'ruzasidagi 4-slayd)
contract Hisob {
    address public egasi;                          // ① holat o'zgaruvchisi
    mapping(address => uint256) public qoldiq;     // ② kalit → qiymat jadvali
    uint256 public jami;

    event Tolov(address indexed kimga, uint256 summa);   // ③ jurnal yozuvi

    modifier faqatEgasi() {                        // ④ kirish nazorati
        require(msg.sender == egasi, "Faqat egasi");
        _;
    }

    constructor() {
        egasi = msg.sender;                        // deploy qilgan kishi — egasi
    }

    /// ⑤ Holatni o'zgartiradi → tranzaksiya, gaz
    function tolash(address kimga, uint256 summa) external faqatEgasi {
        require(kimga != address(0), "Manzil bosh");
        require(summa > 0, "Summa nol");
        qoldiq[kimga] += summa;
        jami += summa;
        emit Tolov(kimga, summa);
    }

    /// ⑥ Faqat o'qiydi → bepul chaqiruv (view)
    function meningQoldigim() external view returns (uint256) {
        return qoldiq[msg.sender];
    }
}
