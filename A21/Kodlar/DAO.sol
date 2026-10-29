// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title UniChainDAO — A21: a'zolik Merkle root orqali (A3), taklif, ovoz, kvorum va kechiktirilgan ijro
/// A'zolar ro'yxati blokcheynda saqlanmaydi — faqat 32 baytlik root. Har bir a'zo o'z proof'i bilan kiradi.
contract DAO {
    bytes32 public immutable azolarRoot;      // A3 dagi 3_merkle_royxat.py chiqargan MERKLE ROOT
    uint256 public immutable ovozMuddati;     // soniya: taklif necha vaqt ovozga qo'yiladi
    uint256 public immutable kechikish;       // soniya: qabul qilingach, ijrodan oldin kutish (timelock)
    uint256 public immutable kvorum;          // kamida nechta a'zo ovoz berishi kerak

    enum Ovoz { Yoq, Ha, Betaraf }

    struct Taklif {
        address muallif;
        string tavsif;
        address maqsad;          // ijro etiladigan chaqiruv: kimga
        uint256 qiymat;          //   qancha ETH (xazinadan)
        bytes data;              //   qaysi funksiya va parametrlar
        uint256 tugash;          // ovoz berish tugaydigan vaqt
        uint256 ha;
        uint256 yoq;
        uint256 betaraf;
        bool bajarildi;
    }

    Taklif[] public takliflar;
    mapping(uint256 => mapping(address => bool)) public ovozBergan;

    event TaklifKiritildi(uint256 indexed id, address indexed muallif, string tavsif, uint256 tugash);
    event OvozBerildi(uint256 indexed id, address indexed kim, Ovoz ovoz);
    event Bajarildi(uint256 indexed id, bool muvaffaqiyat);

    constructor(bytes32 root, uint256 _ovozMuddati, uint256 _kechikish, uint256 _kvorum) {
        azolarRoot = root;
        ovozMuddati = _ovozMuddati;
        kechikish = _kechikish;
        kvorum = _kvorum;
    }

    receive() external payable {}                         // xazina: DAO ga yuborilgan ETH

    modifier faqatAzo(bytes32[] calldata proof) {
        require(azomi(msg.sender, proof), "Azo emas");
        _;
    }

    /// A3 dagi barg formulasi: keccak256(bytes.concat(keccak256(abi.encode(addr)))), juftliklar tartiblangan
    function azomi(address kim, bytes32[] calldata proof) public view returns (bool) {
        bytes32 h = keccak256(bytes.concat(keccak256(abi.encode(kim))));
        for (uint256 i = 0; i < proof.length; i++) {
            h = h < proof[i] ? keccak256(abi.encodePacked(h, proof[i])) : keccak256(abi.encodePacked(proof[i], h));
        }
        return h == azolarRoot;
    }

    function taklifKirit(string calldata tavsif, address maqsad, uint256 qiymat, bytes calldata data,
                         bytes32[] calldata proof) external faqatAzo(proof) returns (uint256 id) {
        id = takliflar.length;
        Taklif storage t = takliflar.push();
        t.muallif = msg.sender;
        t.tavsif = tavsif;
        t.maqsad = maqsad;
        t.qiymat = qiymat;
        t.data = data;
        t.tugash = block.timestamp + ovozMuddati;
        emit TaklifKiritildi(id, msg.sender, tavsif, t.tugash);
    }

    function ovozBer(uint256 id, Ovoz ovoz, bytes32[] calldata proof) external faqatAzo(proof) {
        Taklif storage t = takliflar[id];
        require(block.timestamp < t.tugash, "Ovoz yopilgan");
        require(!ovozBergan[id][msg.sender], "Allaqachon ovoz bergan");
        ovozBergan[id][msg.sender] = true;
        if (ovoz == Ovoz.Ha) t.ha++;
        else if (ovoz == Ovoz.Yoq) t.yoq++;
        else t.betaraf++;
        emit OvozBerildi(id, msg.sender, ovoz);
    }

    /// 0 — ovoz davom etmoqda, 1 — rad etildi, 2 — qabul qilindi (kechikish davri), 3 — ijroga tayyor, 4 — bajarilgan
    function holat(uint256 id) public view returns (uint8) {
        Taklif storage t = takliflar[id];
        if (t.bajarildi) return 4;
        if (block.timestamp < t.tugash) return 0;
        if (t.ha + t.yoq + t.betaraf < kvorum || t.ha <= t.yoq) return 1;
        if (block.timestamp < t.tugash + kechikish) return 2;
        return 3;
    }

    /// Istalgan kishi chaqira oladi — qaror allaqachon qabul qilingan
    function bajar(uint256 id) external {
        require(holat(id) == 3, "Ijroga tayyor emas");
        Taklif storage t = takliflar[id];
        t.bajarildi = true;                                   // avval holat (A12, 12.4)
        (bool ok, ) = t.maqsad.call{value: t.qiymat}(t.data);
        require(ok, "Ijro xato");
        emit Bajarildi(id, ok);
    }

    function takliflarSoni() external view returns (uint256) {
        return takliflar.length;
    }
}
