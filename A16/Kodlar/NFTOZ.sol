// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// A16 · Remix uchun: xuddi shu NFT OpenZeppelin kutubxonasi bilan
import {ERC721, ERC721URIStorage} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract NFTOZ is ERC721URIStorage, Ownable {
    uint256 public jami;

    constructor() ERC721("UniChain Sertifikat OZ", "UNISZ") Ownable(msg.sender) {}

    function mint(address to, string calldata uri) external onlyOwner returns (uint256 id) {
        id = ++jami;
        _safeMint(to, id);
        _setTokenURI(id, uri);
    }
}
