// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {PackedUserOperation} from "./MiniEntryPoint.sol";

/// @title MiniHomiy — A18: paymaster. Ro'yxatdagi akkauntlarning gazini o'zi to'laydi (“gazsiz” tranzaksiya)
/// Masalan, universitet talabalar akkauntlari uchun gazni homiylik qiladi — talabada ETH bo'lishi shart emas.
contract MiniHomiy {
    address public immutable entryPoint;
    address public immutable egasi;
    mapping(address => bool) public homiylikda;

    constructor(address _entryPoint) {
        entryPoint = _entryPoint;
        egasi = msg.sender;
    }

    function qosh(address akkaunt, bool holat) external {
        require(msg.sender == egasi, "Faqat egasi");
        homiylikda[akkaunt] = holat;
    }

    /// 0 — roziman, gazni to'layman; 1 — rad
    function validatePaymasterUserOp(PackedUserOperation calldata op, bytes32, uint256)
        external view returns (bytes memory, uint256)
    {
        require(msg.sender == entryPoint, "Faqat EntryPoint");
        return ("", homiylikda[op.sender] ? 0 : 1);
    }
}
