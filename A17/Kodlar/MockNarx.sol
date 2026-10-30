// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title MockNarx — A17: mahalliy sinov uchun soxta narx manbai (Chainlink interfeysi bilan bir xil)
/// Remix VM va testlarda haqiqiy oracle yo'q — narxni qo'lda o'rnatamiz.
contract MockNarx {
    uint8 public decimals;
    string public description = "ETH / USD (mock)";
    uint80 public roundId;
    int256 public javob;
    uint256 public yangilangan;

    constructor(uint8 _decimals, int256 boshlangich) {
        decimals = _decimals;
        narxniOrnat(boshlangich);
    }

    function narxniOrnat(int256 yangi) public {
        roundId += 1;
        javob = yangi;
        yangilangan = block.timestamp;
    }

    /// Vaqtni sun'iy ravishda o'tmishga surish — “eskirgan narx” holatini sinash uchun
    function yoshiniOrnat(uint256 necha_soniya_oldin) external {
        yangilangan = block.timestamp - necha_soniya_oldin;
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (roundId, javob, yangilangan, yangilangan, roundId);
    }
}
