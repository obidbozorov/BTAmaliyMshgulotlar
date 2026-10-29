// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Tanga — A20: sinov uchun oddiy ERC-20, har kim o'ziga “kran”dan token olishi mumkin
/// Faqat testnet va Remix VM uchun! Real tokenda erkin mint bo'lmaydi.
contract Tanga {
    string public name;
    string public symbol;
    uint8 public constant decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }

    function kran(uint256 value) external {          // faucet: 1 000 000 tokengacha
        require(value <= 1_000_000 * 10 ** decimals, "Kop");
        totalSupply += value;
        balanceOf[msg.sender] += value;
        emit Transfer(address(0), msg.sender, value);
    }

    function approve(address s, uint256 v) external returns (bool) {
        allowance[msg.sender][s] = v;
        emit Approval(msg.sender, s, v);
        return true;
    }

    function transfer(address to, uint256 v) external returns (bool) {
        _otkaz(msg.sender, to, v);
        return true;
    }

    function transferFrom(address from, address to, uint256 v) external returns (bool) {
        require(allowance[from][msg.sender] >= v, "Ruxsat yetarli emas");
        allowance[from][msg.sender] -= v;
        _otkaz(from, to, v);
        return true;
    }

    function _otkaz(address from, address to, uint256 v) internal {
        require(balanceOf[from] >= v, "Balans yetarli emas");
        balanceOf[from] -= v;
        balanceOf[to] += v;
        emit Transfer(from, to, v);
    }
}
