// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// Kontrakt NFT qabul qila olishini bildiruvchi interfeys (safeTransferFrom tekshiradi)
interface IERC721Receiver {
    function onERC721Received(address operator, address from, uint256 tokenId, bytes calldata data)
        external returns (bytes4);
}

/// @title UniChain Sertifikat (UNIS) — A16: ERC-721 standartini noldan yozish
/// @notice O'quv kontrakti. Real loyihada OpenZeppelin ERC721URIStorage dan foydalaning (NFTOZ.sol).
contract NFT {
    string public name = "UniChain Sertifikat";
    string public symbol = "UNIS";
    uint256 public constant MAKS = 100;          // maksimal emissiya — kamyoblik shu yerda belgilanadi
    address public egasi;
    uint256 public jami;                          // chiqarilgan tokenlar soni

    mapping(uint256 => address) private _egalar;           // tokenId → egasi
    mapping(address => uint256) private _balans;           // manzil → nechta NFT
    mapping(uint256 => address) private _ruxsat;           // tokenId → bitta token uchun ruxsat
    mapping(address => mapping(address => bool)) private _operator;   // butun kolleksiyaga ruxsat (A6!)
    mapping(uint256 => string) private _uri;               // tokenId → "ipfs://<CID>"

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    constructor() { egasi = msg.sender; }

    // ERC-165: kontrakt qaysi interfeyslarni qo'llashini e'lon qiladi (hamyon va marketplace shuni so'raydi)
    function supportsInterface(bytes4 id) external pure returns (bool) {
        return id == 0x01ffc9a7      // ERC-165
            || id == 0x80ac58cd      // ERC-721
            || id == 0x5b5e139f;     // ERC-721 Metadata (name, symbol, tokenURI)
    }

    function balanceOf(address a) external view returns (uint256) {
        require(a != address(0), "Manzil bosh");
        return _balans[a];
    }

    function ownerOf(uint256 id) public view returns (address e) {
        e = _egalar[id];
        require(e != address(0), "Token yoq");
    }

    function tokenURI(uint256 id) external view returns (string memory) {
        ownerOf(id);                                   // mavjudligini tekshiradi
        return _uri[id];
    }

    function approve(address to, uint256 id) external {
        address e = ownerOf(id);
        require(msg.sender == e || _operator[e][msg.sender], "Ruxsat yoq");
        _ruxsat[id] = to;
        emit Approval(e, to, id);
    }

    function getApproved(uint256 id) external view returns (address) {
        ownerOf(id);
        return _ruxsat[id];
    }

    function setApprovalForAll(address operator, bool ruxsat) external {
        _operator[msg.sender][operator] = ruxsat;
        emit ApprovalForAll(msg.sender, operator, ruxsat);
    }

    function isApprovedForAll(address e, address operator) external view returns (bool) {
        return _operator[e][operator];
    }

    function transferFrom(address from, address to, uint256 id) public {
        address e = ownerOf(id);
        require(e == from, "Egasi emas");
        require(to != address(0), "Manzil bosh");
        require(msg.sender == e || _ruxsat[id] == msg.sender || _operator[e][msg.sender], "Ruxsat yoq");
        delete _ruxsat[id];                            // egasi almashsa, eski ruxsat bekor bo'ladi
        _balans[from] -= 1;
        _balans[to] += 1;
        _egalar[id] = to;
        emit Transfer(from, to, id);
    }

    function safeTransferFrom(address from, address to, uint256 id) external {
        safeTransferFrom(from, to, id, "");
    }

    /// Oluvchi kontrakt bo'lsa, u NFT ni qabul qila olishini tasdiqlashi shart — aks holda NFT “qulflanib” qoladi
    function safeTransferFrom(address from, address to, uint256 id, bytes memory data) public {
        transferFrom(from, to, id);
        if (to.code.length > 0) {
            require(IERC721Receiver(to).onERC721Received(msg.sender, from, id, data)
                    == IERC721Receiver.onERC721Received.selector, "Qabul qilmaydi");
        }
    }

    /// Yangi sertifikat chiqarish: metama'lumot IPFS'da, blokcheynda faqat uning manzili (CID)
    function mint(address to, string calldata uri) external returns (uint256 id) {
        require(msg.sender == egasi, "Faqat egasi");
        require(to != address(0), "Manzil bosh");
        require(jami < MAKS, "Emissiya tugagan");
        id = ++jami;
        _egalar[id] = to;
        _balans[to] += 1;
        _uri[id] = uri;
        emit Transfer(address(0), to, id);
    }
}
