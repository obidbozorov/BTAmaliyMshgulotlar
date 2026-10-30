// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// Chainlink Data Feed interfeysi (rasmiy AggregatorV3Interface ning kerakli qismi)
interface AggregatorV3Interface {
    function decimals() external view returns (uint8);
    function description() external view returns (string memory);
    function latestRoundData() external view returns (
        uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound);
}

/// @title ChiptaSotuvi — A17: narxi dollarda belgilangan chiptani ETH bilan sotish (oracle orqali)
/// Sepolia'da ETH/USD manbasi: 0x694AA1769357215DE4FAC081bf1f309aDC325306
contract ChiptaSotuvi {
    AggregatorV3Interface public immutable narxManbai;
    address public immutable egasi;
    uint256 public immutable chiptaUSD;        // 18 kasrli dollar: 5 USD = 5e18
    uint256 public immutable maksYosh;         // narx necha soniyadan eski bo'lsa rad etiladi
    mapping(address => uint256) public chiptalar;

    event Sotildi(address indexed xaridor, uint256 tolanganWei, int256 ethNarxi);

    constructor(address manba, uint256 _chiptaUSD, uint256 _maksYosh) {
        narxManbai = AggregatorV3Interface(manba);
        egasi = msg.sender;
        chiptaUSD = _chiptaUSD;
        maksYosh = _maksYosh;
    }

    /// Oracle javobini tekshirib, 1 ETH narxini 18 kasrli dollarda qaytaradi
    function ethNarxi() public view returns (uint256 narx18, int256 xom) {
        (uint80 roundId, int256 javob, , uint256 yangilangan, uint80 javobRaund) = narxManbai.latestRoundData();
        require(javob > 0, "Narx notogri");
        require(yangilangan != 0 && javobRaund >= roundId, "Raund tugallanmagan");
        require(block.timestamp - yangilangan <= maksYosh, "Narx eskirgan");
        uint8 d = narxManbai.decimals();                       // Chainlink USD manbalarida odatda 8
        narx18 = d <= 18 ? uint256(javob) * 10 ** (18 - d) : uint256(javob) / 10 ** (d - 18);
        xom = javob;
    }

    /// Chipta uchun kerakli ETH (wei): chiptaUSD / ethNarxi
    function kerakliWei() public view returns (uint256) {
        (uint256 narx18, ) = ethNarxi();
        return (chiptaUSD * 1e18 + narx18 - 1) / narx18;      // yuqoriga yaxlitlash — sotuvchi zarar ko'rmaydi
    }

    function sotibOl() external payable {
        uint256 kerak = kerakliWei();
        require(msg.value >= kerak, "ETH yetarli emas");
        chiptalar[msg.sender] += 1;
        (, int256 xom) = ethNarxi();
        emit Sotildi(msg.sender, kerak, xom);
        if (msg.value > kerak) {                                // ortiqchasini qaytarish
            (bool ok, ) = msg.sender.call{value: msg.value - kerak}("");
            require(ok, "Qaytarish xato");
        }
    }

    function yechib(address payable kimga) external {
        require(msg.sender == egasi, "Faqat egasi");
        (bool ok, ) = kimga.call{value: address(this).balance}("");
        require(ok, "Otkazma xato");
    }
}
