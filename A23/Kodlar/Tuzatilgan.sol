// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// A23 · Zaif.sol dagi kontraktlarning tuzatilgan variantlari (o'qituvchi uchun namuna yechim)

/// 1) Reentrancy: Checks → Effects → Interactions va qayta kirish qulfi
contract BankTuzatilgan {
    mapping(address => uint256) public balans;
    bool private qulf;

    modifier qaytaKirishYoq() {
        require(!qulf, "Qayta kirish");
        qulf = true;
        _;
        qulf = false;
    }

    function qoy() external payable {
        balans[msg.sender] += msg.value;
    }

    function ol() external qaytaKirishYoq {
        uint256 s = balans[msg.sender];
        require(s > 0, "Balans yoq");
        balans[msg.sender] = 0;                          // avval holat
        (bool ok, ) = msg.sender.call{value: s}("");     // keyin tashqi chaqiruv
        require(ok, "Otkazma xato");
    }
}

/// 2) tx.origin o'rniga msg.sender
contract HamyonTuzatilgan {
    address public egasi;

    constructor() payable { egasi = msg.sender; }

    function yubor(address payable kimga, uint256 summa) external {
        require(msg.sender == egasi, "Faqat egasi");
        kimga.transfer(summa);
    }

    receive() external payable {}
}

/// 3) mint faqat egasiga
contract TokenTuzatilgan {
    address public egasi;
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    constructor() { egasi = msg.sender; }

    function mint(address kimga, uint256 summa) external {
        require(msg.sender == egasi, "Faqat egasi");
        balanceOf[kimga] += summa;
        totalSupply += summa;
    }

    function transfer(address kimga, uint256 summa) external {
        require(balanceOf[msg.sender] >= summa, "Balans yetarli emas");
        balanceOf[msg.sender] -= summa;
        balanceOf[kimga] += summa;
    }
}

/// 4) unchecked olib tashlandi: ko'paytma to'lib ketsa, Solidity 0.8 tranzaksiyani bekor qiladi (Panic 0x11)
contract OmmaviyTuzatilgan {
    mapping(address => uint256) public balanceOf;

    constructor() { balanceOf[msg.sender] = 1000 ether; }

    function ommaviyOtkaz(address[] calldata oluvchilar, uint256 qiymat) external {
        uint256 jami = oluvchilar.length * qiymat;
        require(balanceOf[msg.sender] >= jami, "Balans yetarli emas");
        balanceOf[msg.sender] -= jami;
        for (uint256 i = 0; i < oluvchilar.length; i++) {
            balanceOf[oluvchilar[i]] += qiymat;
        }
    }
}

/// 5) Commit-reveal: tasodifiy son o'yin yopilgandan keyin oshkor qilinadigan sir'dan olinadi.
/// Eslatma: operatorga hali ham ishonch kerak (sir'ni oshkor qilmasligi mumkin). Eng yaxshi yechim — Chainlink VRF.
contract LotereyaTuzatilgan {
    address public immutable egasi;
    bytes32 public immutable sirXeshi;            // keccak256(abi.encode(sir)) — deploy vaqtida e'lon qilinadi
    uint256 public immutable tugash;
    mapping(address => uint256) public taxmin;
    mapping(address => bool) public oynagan;
    address[] public oyinchilar;
    bool public ochildi;
    uint256 public natija;

    constructor(bytes32 _sirXeshi, uint256 davomiylik) payable {
        egasi = msg.sender;
        sirXeshi = _sirXeshi;
        tugash = block.timestamp + davomiylik;
    }

    function oyna(uint256 t) external payable {
        require(block.timestamp < tugash, "Oyin yopilgan");
        require(msg.value == 0.1 ether, "0.1 ETH tiking");
        require(!oynagan[msg.sender], "Allaqachon oynagan");
        oynagan[msg.sender] = true;
        taxmin[msg.sender] = t;
        oyinchilar.push(msg.sender);
    }

    function ochish(bytes32 sir) external {
        require(msg.sender == egasi, "Faqat egasi");
        require(block.timestamp >= tugash && !ochildi, "Hali erta");
        require(keccak256(abi.encode(sir)) == sirXeshi, "Sir notogri");
        ochildi = true;
        natija = uint256(keccak256(abi.encode(sir, oyinchilar.length))) % 10;
        uint256 yutganlar;
        for (uint256 i = 0; i < oyinchilar.length; i++) if (taxmin[oyinchilar[i]] == natija) yutganlar++;
        if (yutganlar == 0) return;
        uint256 ulush = address(this).balance / yutganlar;
        for (uint256 i = 0; i < oyinchilar.length; i++) {
            if (taxmin[oyinchilar[i]] == natija) payable(oyinchilar[i]).transfer(ulush);
        }
    }
}

/// 6) Push o'rniga pull: qaytariladigan pul yoziladi, egasi o'zi oladi — bitta oluvchi butun auksionni to'xtata olmaydi
contract AuksionTuzatilgan {
    address public yetakchi;
    uint256 public engYuqori;
    mapping(address => uint256) public qaytarish;

    function taklif() external payable {
        require(msg.value > engYuqori, "Taklif past");
        if (yetakchi != address(0)) qaytarish[yetakchi] += engYuqori;
        yetakchi = msg.sender;
        engYuqori = msg.value;
    }

    function qaytibOl() external {
        uint256 s = qaytarish[msg.sender];
        require(s > 0, "Qaytarish yoq");
        qaytarish[msg.sender] = 0;
        (bool ok, ) = msg.sender.call{value: s}("");
        require(ok, "Otkazma xato");
    }
}
