// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
// A14 — beshta mashq SHABLONI. Har bir “TODO” ni to'ldiring, kompilyatsiya qiling va Remix VM'da sinang.

// 1-mashq: hisoblagich
contract Hisoblagich {
    uint256 public son;
    event Ozgardi(address kim, uint256 yangi);
    function oshir() external { /* TODO: son'ni 1 ga oshiring va event chiqaring */ }
    function kamaytir() external { /* TODO: son > 0 ekanini tekshiring ("Son nolga teng"), kamaytiring, event */ }
}

// 2-mashq: talabalar ro'yxati
contract Talabalar {
    struct Talaba { string ism; uint16 kurs; bool bor; }
    mapping(address => Talaba) public royxat;
    uint256 public soni;
    event Qoshildi(address manzil, string ism);
    function royxatdanOt(string calldata ism, uint16 kurs) external {
        // TODO: 1) qayta ro'yxatdan o'tishni taqiqlang  2) kurs 1–4 oralig'ida bo'lsin
        //       3) struct'ni saqlang, soni++, event chiqaring
    }
}

// 3-mashq: ovoz berish
contract Ovoz {
    address public egasi = msg.sender;
    bool public yopiq;
    mapping(address => bool) public berdi;
    uint256 public ha; uint256 public yoq;
    function ovozBer(bool rozi) external { /* TODO: yopiq emasligini va avval ovoz bermaganini tekshiring */ }
    function yakunla() external { /* TODO: faqat egasi yopa olsin */ }
    function natija() external view returns (string memory) { /* TODO */ }
}

// 4-mashq: vaqtli qulf
contract VaqtliQulf {
    mapping(address => uint256) public qoldiq;
    mapping(address => uint256) public ochilish;
    function qoy(uint256 sekund) external payable { /* TODO: ETH qabul qiling, ochilish vaqtini belgilang */ }
    function ol() external { /* TODO: vaqt kelganini tekshiring; AVVAL qoldiqni 0 qiling, KEYIN ETH yuboring */ }
}

// 5-mashq: oq ro'yxat
contract OqRoyxat {
    address public egasi = msg.sender;
    mapping(address => bool) public ruxsat;
    uint256 public kirishlar;
    event Qoshildi(address kim);
    // TODO: faqatEgasi va faqatRuxsatli modifikatorlarini yozing
    function qosh(address kim) external { /* TODO: faqat egasi; ruxsat bering, event */ }
    function kir() external { /* TODO: faqat ruxsatlilar; kirishlar++ */ }
}
