// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ProfiCoin (PRC) — A13 dagi token (A14 da Hardhat bilan testlanadi)
/// @notice O'quv kontrakti. Real loyihada OpenZeppelin ERC20 dan foydalaning (TokenOZ.sol).
contract Token {
    string public name = "ProfiCoin";
    string public symbol = "PRC";
    uint8 public constant decimals = 18;                 // 1 PRC = 10^18 eng kichik birlik
    uint256 public totalSupply;
    address public egasi;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;   // egasi → spender → limit

    // ERC-20 standarti talab qiladigan ikki event
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    modifier faqatEgasi() {
        require(msg.sender == egasi, "Faqat egasi");
        _;
    }

    constructor(uint256 boshlangich) {
        egasi = msg.sender;
        _mint(msg.sender, boshlangich * 10 ** decimals);
    }

    function transfer(address to, uint256 value) external returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        require(spender != address(0), "Spender bosh");
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        uint256 ruxsat = allowance[from][msg.sender];
        require(ruxsat >= value, "Ruxsat yetarli emas");
        if (ruxsat != type(uint256).max) {               // cheksiz ruxsat kamaytirilmaydi (A6)
            allowance[from][msg.sender] = ruxsat - value;
        }
        _transfer(from, to, value);
        return true;
    }

    /// Faqat egasi yangi token chiqaradi — markazlashuv nuqtasi (hisobotda baholang)
    function mint(address to, uint256 value) external faqatEgasi {
        _mint(to, value);
    }

    /// Har kim o'z tokenini yoqishi mumkin: totalSupply kamayadi
    function burn(uint256 value) external {
        require(balanceOf[msg.sender] >= value, "Balans yetarli emas");
        balanceOf[msg.sender] -= value;
        totalSupply -= value;
        emit Transfer(msg.sender, address(0), value);
    }

    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0), "Manzil bosh");
        require(balanceOf[from] >= value, "Balans yetarli emas");
        balanceOf[from] -= value;
        balanceOf[to] += value;
        emit Transfer(from, to, value);
    }

    function _mint(address to, uint256 value) internal {
        require(to != address(0), "Manzil bosh");
        totalSupply += value;
        balanceOf[to] += value;
        emit Transfer(address(0), to, value);       // mint — "0x0 dan o'tkazma"
    }
}
