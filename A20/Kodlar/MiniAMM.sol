// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function transfer(address to, uint256 value) external returns (bool);
}

/// @title MiniAMM — A20: ikki tokenli x·y = k havzasi (Uniswap V2 g'oyasi, soddalashtirilgan)
/// @notice O'quv kontrakti: flash swap, oracle (TWAP) va ko'p havzali marshrut yo'q. Real mablag' uchun emas!
contract MiniAMM {
    IERC20 public immutable tokenA;
    IERC20 public immutable tokenB;
    uint256 public zaxiraA;
    uint256 public zaxiraB;

    uint256 public constant MIN_LIKVIDLIK = 1000;
    uint256 public lpJami;
    mapping(address => uint256) public lpBalans;          // LP “ulush” tokenlari (soddalik uchun ERC-20 emas)

    event LikvidlikQoshildi(address indexed kim, uint256 a, uint256 b, uint256 lp);
    event LikvidlikOlindi(address indexed kim, uint256 a, uint256 b, uint256 lp);
    event Almashtirildi(address indexed kim, bool aDanB, uint256 kirish, uint256 chiqish);

    constructor(address _a, address _b) {
        tokenA = IERC20(_a);
        tokenB = IERC20(_b);
    }

    modifier muddat(uint256 deadline) {
        require(block.timestamp <= deadline, "Muddat otgan");
        _;
    }

    /// Uniswap V2 formulasi: komissiya 0,3% kiruvchi tokendan olinadi
    function chiqishMiqdori(uint256 kirish, uint256 zKirish, uint256 zChiqish) public pure returns (uint256) {
        require(kirish > 0 && zKirish > 0 && zChiqish > 0, "Miqdor yoki zaxira nol");
        uint256 k = kirish * 997;
        return k * zChiqish / (zKirish * 1000 + k);
    }

    function likvidlikQosh(uint256 a, uint256 b, uint256 deadline) external muddat(deadline) returns (uint256 lp) {
        if (lpJami == 0) {
            lp = _sqrt(a * b) - MIN_LIKVIDLIK;
            lpJami = MIN_LIKVIDLIK;                        // abadiy qulflangan qism
        } else {
            uint256 lpA = a * lpJami / zaxiraA;
            uint256 lpB = b * lpJami / zaxiraB;
            lp = lpA < lpB ? lpA : lpB;                    // nisbatni buzgan ortiqcha qism havzaga “sovg'a”
        }
        require(lp > 0, "LP nol");
        _ol(tokenA, a);
        _ol(tokenB, b);
        zaxiraA += a;
        zaxiraB += b;
        lpJami += lp;
        lpBalans[msg.sender] += lp;
        emit LikvidlikQoshildi(msg.sender, a, b, lp);
    }

    function likvidlikOl(uint256 lp, uint256 minA, uint256 minB, uint256 deadline)
        external muddat(deadline) returns (uint256 a, uint256 b)
    {
        require(lpBalans[msg.sender] >= lp, "LP yetarli emas");
        a = lp * zaxiraA / lpJami;
        b = lp * zaxiraB / lpJami;
        require(a >= minA && b >= minB, "Slippage: chiqish kam");
        lpBalans[msg.sender] -= lp;
        lpJami -= lp;
        zaxiraA -= a;
        zaxiraB -= b;
        _ber(tokenA, a);
        _ber(tokenB, b);
        emit LikvidlikOlindi(msg.sender, a, b, lp);
    }

    /// kirish — beriladigan token miqdori; minChiqish — foydalanuvchi qabul qiladigan eng kam miqdor (slippage himoyasi)
    function almashtir(bool aDanB, uint256 kirish, uint256 minChiqish, uint256 deadline)
        external muddat(deadline) returns (uint256 chiqish)
    {
        (IERC20 tIn, IERC20 tOut, uint256 zIn, uint256 zOut) =
            aDanB ? (tokenA, tokenB, zaxiraA, zaxiraB) : (tokenB, tokenA, zaxiraB, zaxiraA);
        chiqish = chiqishMiqdori(kirish, zIn, zOut);
        require(chiqish >= minChiqish, "Slippage: chiqish kam");
        _ol(tIn, kirish);
        _ber(tOut, chiqish);
        if (aDanB) { zaxiraA += kirish; zaxiraB -= chiqish; }
        else       { zaxiraB += kirish; zaxiraA -= chiqish; }
        emit Almashtirildi(msg.sender, aDanB, kirish, chiqish);
    }

    // Token qaytargan bool tekshiriladi (real loyihada OpenZeppelin SafeERC20 ishlatiladi)
    function _ol(IERC20 t, uint256 v) internal { require(t.transferFrom(msg.sender, address(this), v), "Otkazma xato"); }
    function _ber(IERC20 t, uint256 v) internal { require(t.transfer(msg.sender, v), "Otkazma xato"); }

    function _sqrt(uint256 y) internal pure returns (uint256 z) {   // Bobil usuli
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) { z = x; x = (y / x + x) / 2; }
        } else if (y != 0) {
            z = 1;
        }
    }
}
