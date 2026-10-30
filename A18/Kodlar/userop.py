# A18 · ERC-4337 (EntryPoint v0.7) UserOperation: tuzish, xeshlash, imzolash
# O'rnatish: pip install -r requirements.txt
from dataclasses import dataclass, field
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import keccak, to_checksum_address

ENTRYPOINT_V07 = "0x0000000071727De22E5E9d8BAf0edAc6f37da032"     # barcha EVM tarmoqlarida bir xil manzil


@dataclass
class UserOp:
    """PackedUserOperation (v0.7). Oddiy tranzaksiya o'rniga smart-akkaunt nomidan bajariladigan “niyat”."""
    sender: str                         # smart-akkaunt manzili (EOA emas!)
    nonce: int                          # (key << 64) | ketma-ketlik raqami
    callData: bytes                     # akkaunt bajaradigan chaqiruv: execute(dest, value, data)
    verificationGasLimit: int = 150_000
    callGasLimit: int = 100_000
    preVerificationGas: int = 50_000    # bundler xarajati (calldata, imzo tekshiruvidan oldingi ish)
    maxPriorityFeePerGas: int = 10**9
    maxFeePerGas: int = 2 * 10**9
    initCode: bytes = b""               # akkaunt hali deploy qilinmagan bo'lsa: factory manzili + chaqiruv
    paymasterAndData: bytes = b""       # gazni boshqa kishi to'lasa: paymaster manzili + ma'lumot
    signature: bytes = b""

    # v0.7 da ikki gaz maydoni bitta bytes32 ga “qadoqlanadi”
    def accountGasLimits(self) -> bytes:
        return ((self.verificationGasLimit << 128) | self.callGasLimit).to_bytes(32, "big")

    def gasFees(self) -> bytes:
        return ((self.maxPriorityFeePerGas << 128) | self.maxFeePerGas).to_bytes(32, "big")

    def kortej(self):
        """Solidity'ga PackedUserOperation struct sifatida yuborish uchun"""
        return (to_checksum_address(self.sender), self.nonce, self.initCode, self.callData, self.accountGasLimits(),
                self.preVerificationGas, self.gasFees(), self.paymasterAndData, self.signature)


def userop_hash(op: UserOp, entry_point: str, chain_id: int) -> bytes:
    """EntryPoint v0.7 getUserOpHash bilan bir xil: imzo bundan tashqari, entryPoint va chainId qo'shiladi"""
    ichki = keccak(encode(
        ["address", "uint256", "bytes32", "bytes32", "bytes32", "uint256", "bytes32", "bytes32"],
        [op.sender, op.nonce, keccak(op.initCode), keccak(op.callData), op.accountGasLimits(),
         op.preVerificationGas, op.gasFees(), keccak(op.paymasterAndData)]))
    return keccak(encode(["bytes32", "address", "uint256"], [ichki, entry_point, chain_id]))


def imzola(op: UserOp, kalit: str, entry_point: str, chain_id: int) -> UserOp:
    """SimpleAccount uslubi: userOpHash ga EIP-191 (personal_sign) imzosi, A4 dagi kabi"""
    h = userop_hash(op, entry_point, chain_id)
    op.signature = bytes(Account.sign_message(encode_defunct(h), kalit).signature)
    return op


def execute_calldata(dest: str, value: int, data: bytes = b"") -> bytes:
    """MiniHisob.execute(address,uint256,bytes) chaqiruvi"""
    return keccak(b"execute(address,uint256,bytes)")[:4] + encode(["address", "uint256", "bytes"], [dest, value, data])


def batch_calldata(chaqiruvlar) -> bytes:
    """MiniHisob.executeBatch(address[],uint256[],bytes[]) — bir nechta amal bitta UserOp'da"""
    d, v, b = zip(*chaqiruvlar)
    return keccak(b"executeBatch(address[],uint256[],bytes[])")[:4] + encode(["address[]", "uint256[]", "bytes[]"], [list(d), list(v), list(b)])
