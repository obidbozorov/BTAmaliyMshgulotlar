// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
// A12 — beshta mashqning YECHIMI (o'qituvchi uchun)

// 1-mashq: hisoblagich — require va event
contract Hisoblagich {
    uint256 public son;
    event Ozgardi(address kim, uint256 yangi);
    function oshir() external { son += 1; emit Ozgardi(msg.sender, son); }
    function kamaytir() external {
        require(son > 0, "Son nolga teng");
        son -= 1; emit Ozgardi(msg.sender, son);
    }
}

// 2-mashq: talabalar ro'yxati — struct va mapping
contract Talabalar {
    struct Talaba { string ism; uint16 kurs; bool bor; }
    mapping(address => Talaba) public royxat;
    uint256 public soni;
    event Qoshildi(address manzil, string ism);
    function royxatdanOt(string calldata ism, uint16 kurs) external {
        require(!royxat[msg.sender].bor, "Allaqachon royxatda");
        require(kurs >= 1 && kurs <= 4, "Kurs 1-4");
        royxat[msg.sender] = Talaba(ism, kurs, true);
        soni++; emit Qoshildi(msg.sender, ism);
    }
}

// 3-mashq: ovoz berish — har kim bir marta, egasi yakunlaydi
contract Ovoz {
    address public egasi = msg.sender;
    bool public yopiq;
    mapping(address => bool) public berdi;
    uint256 public ha; uint256 public yoq;
    function ovozBer(bool rozi) external {
        require(!yopiq, "Ovoz yopilgan");
        require(!berdi[msg.sender], "Siz ovoz bergansiz");
        berdi[msg.sender] = true;
        if (rozi) ha++; else yoq++;
    }
    function yakunla() external { require(msg.sender == egasi, "Faqat egasi"); yopiq = true; }
    function natija() external view returns (string memory) { return ha > yoq ? "Qabul qilindi" : "Rad etildi"; }
}

// 4-mashq: vaqtli qulf — ETH faqat belgilangan vaqtdan keyin qaytariladi
contract VaqtliQulf {
    mapping(address => uint256) public qoldiq;
    mapping(address => uint256) public ochilish;
    function qoy(uint256 sekund) external payable {
        require(msg.value > 0, "ETH yuboring");
        qoldiq[msg.sender] += msg.value;
        ochilish[msg.sender] = block.timestamp + sekund;
    }
    function ol() external {
        require(block.timestamp >= ochilish[msg.sender], "Hali erta");
        uint256 s = qoldiq[msg.sender];
        require(s > 0, "Qoldiq yoq");
        qoldiq[msg.sender] = 0;                    // avval holat,
        (bool ok, ) = msg.sender.call{value: s}(""); // keyin o'tkazma
        require(ok, "Otkazma xato");
    }
}

// 5-mashq: oq ro'yxat — o'z modifikatoringiz
contract OqRoyxat {
    address public egasi = msg.sender;
    mapping(address => bool) public ruxsat;
    uint256 public kirishlar;
    event Qoshildi(address kim);
    modifier faqatEgasi() { require(msg.sender == egasi, "Faqat egasi"); _; }
    modifier faqatRuxsatli() { require(ruxsat[msg.sender], "Royxatda yoq"); _; }
    function qosh(address kim) external faqatEgasi { ruxsat[kim] = true; emit Qoshildi(kim); }
    function kir() external faqatRuxsatli { kirishlar++; }
}
