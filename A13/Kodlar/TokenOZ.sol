// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// A13 · Remix uchun: xuddi shu token OpenZeppelin kutubxonasi bilan (Remix importni npm'dan o'zi yuklaydi)
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract TokenOZ is ERC20, Ownable {
    constructor(uint256 boshlangich) ERC20("ProfiCoin OZ", "PRCZ") Ownable(msg.sender) {
        _mint(msg.sender, boshlangich * 10 ** decimals());
    }

    function mint(address to, uint256 value) external onlyOwner {
        _mint(to, value);
    }
}
