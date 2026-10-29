// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// ERC-4337 v0.7 dagi PackedUserOperation tuzilmasi (real EntryPoint bilan bir xil)
struct PackedUserOperation {
    address sender;
    uint256 nonce;
    bytes initCode;
    bytes callData;
    bytes32 accountGasLimits;     // verificationGasLimit (yuqori 128 bit) | callGasLimit (quyi 128 bit)
    uint256 preVerificationGas;
    bytes32 gasFees;              // maxPriorityFeePerGas (yuqori) | maxFeePerGas (quyi)
    bytes paymasterAndData;
    bytes signature;
}

interface IAkkaunt {
    function validateUserOp(PackedUserOperation calldata op, bytes32 userOpHash, uint256 tolanmagan)
        external returns (uint256 validationData);
}

interface IPaymaster {
    function validatePaymasterUserOp(PackedUserOperation calldata op, bytes32 userOpHash, uint256 maksXarajat)
        external returns (bytes memory context, uint256 validationData);
}

/// @title MiniEntryPoint — A18: ERC-4337 EntryPoint'ning o'quv modeli
/// @notice Real EntryPoint (0x0000000071727De22E5E9d8BAf0edAc6f37da032) ning asosiy mantiqi: depozit, nonce,
///         tekshiruv bosqichi, ijro bosqichi va gaz uchun to'lov. Soddalashtirilgan: initCode, imzo agregatsiyasi,
///         postOp va gaz limitlarining qat'iy nazorati yo'q. Faqat o'qish uchun — real loyihada ishlatmang!
contract MiniEntryPoint {
    mapping(address => uint256) public balanceOf;                         // depozitlar (akkaunt va paymaster)
    mapping(address => mapping(uint192 => uint256)) public nonceSequenceNumber;

    event Deposited(address indexed account, uint256 totalDeposit);
    event UserOperationEvent(bytes32 indexed userOpHash, address indexed sender, address indexed paymaster,
                             uint256 nonce, bool success, uint256 actualGasCost, uint256 actualGasUsed);

    error FailedOp(uint256 opIndex, string reason);

    function depositTo(address account) external payable {
        balanceOf[account] += msg.value;
        emit Deposited(account, balanceOf[account]);
    }

    function getNonce(address sender, uint192 key) external view returns (uint256) {
        return nonceSequenceNumber[sender][key] | (uint256(key) << 64);
    }

    /// Real EntryPoint v0.7 getUserOpHash bilan bir xil formula (userop.py bilan solishtiriladi)
    function getUserOpHash(PackedUserOperation calldata op) public view returns (bytes32) {
        bytes32 ichki = keccak256(abi.encode(
            op.sender, op.nonce, keccak256(op.initCode), keccak256(op.callData),
            op.accountGasLimits, op.preVerificationGas, op.gasFees, keccak256(op.paymasterAndData)));
        return keccak256(abi.encode(ichki, address(this), block.chainid));
    }

    /// Bundler bir nechta UserOp'ni bitta tranzaksiyada yuboradi va gaz uchun kompensatsiyani `beneficiary` oladi
    function handleOps(PackedUserOperation[] calldata ops, address payable beneficiary) external {
        uint256 jamiKompensatsiya;
        for (uint256 i = 0; i < ops.length; i++) {
            jamiKompensatsiya += _bitta(i, ops[i]);
        }
        (bool ok, ) = beneficiary.call{value: jamiKompensatsiya}("");
        require(ok, "Kompensatsiya xato");
    }

    function _bitta(uint256 i, PackedUserOperation calldata op) internal returns (uint256 xarajat) {
        uint256 boshGaz = gasleft();
        (bytes32 h, address paymaster) = _tekshiruv(i, op);

        // 4) ijro bosqichi: xato bo'lsa ham UserOp “ishlatilgan” hisoblanadi va gaz to'lanadi
        (bool muvaffaqiyat, ) = op.sender.call{gas: uint128(uint256(op.accountGasLimits))}(op.callData);

        // 5) haqiqiy xarajat: ishlatilgan gaz × samarali narx (A7 dagi EIP-1559 formulasi)
        uint256 ishlatilgan = boshGaz - gasleft() + op.preVerificationGas;
        xarajat = ishlatilgan * _narx(op);
        balanceOf[paymaster == address(0) ? op.sender : paymaster] -= xarajat;
        emit UserOperationEvent(h, op.sender, paymaster, op.nonce, muvaffaqiyat, xarajat, ishlatilgan);
    }

    function _tekshiruv(uint256 i, PackedUserOperation calldata op) internal returns (bytes32 h, address paymaster) {
        h = getUserOpHash(op);

        // 1) nonce: kalit bo'yicha ketma-ketlik — replay himoyasi
        uint192 key = uint192(op.nonce >> 64);
        if (uint64(op.nonce) != nonceSequenceNumber[op.sender][key]++) revert FailedOp(i, "AA25 invalid account nonce");

        // 2) eng ko'p to'lanishi mumkin bo'lgan summa: barcha gaz limitlari × maxFeePerGas
        uint256 maksXarajat = (uint128(uint256(op.accountGasLimits) >> 128) + uint128(uint256(op.accountGasLimits))
                               + op.preVerificationGas) * uint128(uint256(op.gasFees));

        // 3) tekshiruv bosqichi: kim to'laydi — akkauntmi yoki paymaster?
        if (op.paymasterAndData.length >= 20) paymaster = address(bytes20(op.paymasterAndData[:20]));
        address tolovchi = paymaster == address(0) ? op.sender : paymaster;
        uint256 tolanmagan = paymaster != address(0) || balanceOf[op.sender] >= maksXarajat ? 0 : maksXarajat - balanceOf[op.sender];
        if (IAkkaunt(op.sender).validateUserOp(op, h, tolanmagan) != 0) revert FailedOp(i, "AA24 signature error");
        if (paymaster != address(0)) {
            (, uint256 pv) = IPaymaster(paymaster).validatePaymasterUserOp(op, h, maksXarajat);
            if (pv != 0) revert FailedOp(i, "AA34 signature error");
        }
        if (balanceOf[tolovchi] < maksXarajat) {
            revert FailedOp(i, tolovchi == op.sender ? "AA21 didn't pay prefund" : "AA31 paymaster deposit too low");
        }
    }

    function _narx(PackedUserOperation calldata op) internal view returns (uint256 narx) {
        narx = uint128(uint256(op.gasFees));                                   // maxFeePerGas
        uint256 tip = uint128(uint256(op.gasFees) >> 128);                     // maxPriorityFeePerGas
        if (block.basefee + tip < narx) narx = block.basefee + tip;
    }

    receive() external payable {
        balanceOf[msg.sender] += msg.value;            // akkaunt validateUserOp ichida yuborgan prefund
    }
}
