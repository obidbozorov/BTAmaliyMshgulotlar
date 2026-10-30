// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {PackedUserOperation} from "./MiniEntryPoint.sol";

/// @title MiniHisob — A18: smart-akkaunt (SimpleAccount uslubida)
/// Pul va tokenlar shu kontraktda turadi; egasining kaliti faqat “niyat”ni (UserOp) imzolaydi.
contract MiniHisob {
    address public immutable entryPoint;
    address public egasi;

    event EgasiAlmashdi(address eski, address yangi);

    constructor(address _entryPoint, address _egasi) {
        entryPoint = _entryPoint;
        egasi = _egasi;
    }

    modifier faqatEntryPointYokiEgasi() {
        require(msg.sender == entryPoint || msg.sender == egasi, "Ruxsat yoq");
        _;
    }

    /// EntryPoint chaqiradi: imzo to'g'rimi? 0 — ha, 1 — yo'q (SIG_VALIDATION_FAILED)
    function validateUserOp(PackedUserOperation calldata op, bytes32 userOpHash, uint256 tolanmagan)
        external returns (uint256)
    {
        require(msg.sender == entryPoint, "Faqat EntryPoint");
        uint256 natija = _imzoEgasi(userOpHash, op.signature) == egasi ? 0 : 1;
        if (tolanmagan > 0) {                                   // depozit yetmasa, akkaunt o'zi to'laydi
            (bool ok, ) = payable(msg.sender).call{value: tolanmagan}("");
            ok;
        }
        return natija;
    }

    function execute(address dest, uint256 value, bytes calldata data) external faqatEntryPointYokiEgasi {
        _chaqir(dest, value, data);
    }

    /// Bir nechta amal bitta UserOp'da va atomar: biri xato bo'lsa, hammasi bekor
    function executeBatch(address[] calldata dest, uint256[] calldata value, bytes[] calldata data)
        external faqatEntryPointYokiEgasi
    {
        require(dest.length == value.length && dest.length == data.length, "Uzunlik xato");
        for (uint256 i = 0; i < dest.length; i++) _chaqir(dest[i], value[i], data[i]);
    }

    /// Kalit yo'qolsa ham akkaunt saqlanadi: egasini almashtirish (ijtimoiy tiklash g'oyasi)
    function egasiniAlmashtir(address yangi) external {
        require(msg.sender == address(this), "Faqat UserOp orqali");
        emit EgasiAlmashdi(egasi, yangi);
        egasi = yangi;
    }

    function _chaqir(address dest, uint256 value, bytes calldata data) internal {
        (bool ok, bytes memory javob) = dest.call{value: value}(data);
        if (!ok) assembly { revert(add(javob, 32), mload(javob)) }
    }

    /// EIP-191 (personal_sign) imzosidan manzilni tiklash — A4 dagi 4.4 bilan bir xil g'oya
    function _imzoEgasi(bytes32 h, bytes calldata sig) internal pure returns (address) {
        if (sig.length != 65) return address(0);
        bytes32 r = bytes32(sig[0:32]);
        bytes32 s = bytes32(sig[32:64]);
        uint8 v = uint8(sig[64]);
        if (uint256(s) > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0) return address(0);  // EIP-2
        return ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", h)), v, r, s);
    }

    receive() external payable {}
}
