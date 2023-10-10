// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/ERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/utils/Counters.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/IERC20.sol";


contract MusicNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    IERC20 public immutable USDC;

    uint256 public immutable maxNFT;

    uint256 public NFTPriceInUSDC;

    // Event to be emited ones we mint new NFT token
    event newNFTMinted(uint256 numberOfNFT, address owner);

    // Event to be emited ones new price is setted
    event newPrice(string message, uint256 newPrice);

    constructor(address _usdc, uint256 _maxNft) ERC721("MuscialNFT", "MFT") {
        // instatiating mock ERC20 token (that we previusly deployed)
        USDC = IERC20(_usdc);    
        // Defining maximum number of tokens this contract cna mint
        maxNFT = _maxNft;     
    }



    /** 
        This function is used for minting new NFTs. We need to pass token uri (uniform resource 
        Identifier) from IPFS (via Pinata).  Metadata of some NFT is basically 
        detail explanation of NFT content: characteristic, link to song in our 
        case and other relevant information. Second argument that we need to pass is number of 
        NFTs we want to buy
    */

    // For crypto buyers
    function buyNFT(string memory uri, uint256 nftCount) public {
        // Here we are cheking if desired number of NFTs is bigger then one
        require(nftCount > 0, "You have to mint at least one Track Pack NFT.");
        // Here we are cheking if number of already minted NFT is bigger then max allowed to be minted
        require(nftCount + _tokenIdCounter.current() <= maxNFT, "There aren't enough Track Pack NFTs for this drop for you to mint you amount you chose. Another drop will be available soon!");
        // Here we check if user balance in MockUSDC is bigger the number NFTs he want to buy * price of NFTs
        require(USDC.balanceOf(msg.sender) >= NFTPriceInUSDC * nftCount, "You don't have enough USDC to pay for the Track Pack NFT(s).");
        // Check if total amount of approved MOckUSDC to this contract tokens is bigger then number of NFTs * price  
        require(USDC.allowance(msg.sender, address(this)) >= NFTPriceInUSDC * nftCount, "You haven't approved this contract to spend enough of your USDC to pay for the Track Pack NFT(s).");
        // If everything goes ok then make MockUSDC tokens transfer from user account to this contract
        USDC.transferFrom(msg.sender, address(this), NFTPriceInUSDC * nftCount);
        // Take new NFT token ID
        for (uint256 x = 0; x < nftCount; x++) {
            uint256 tokenId = _tokenIdCounter.current();
            // Increment counter
            _tokenIdCounter.increment();
            // Mint new token
            _safeMint(msg.sender, tokenId);
            // Set new token URI to token ID
            _setTokenURI(tokenId, uri);
            // Emit event about succesful minting
            emit newNFTMinted(tokenId, msg.sender);
        }
    }
    
    // When credit card buyers buy new NFT we need to mint to custodial wallet. Same as beafore. Diffrence is: onnly owner can mint, 2. there is no need to pay in usdc
    // it is already done by credit card. 
    function createNFT(address custodialWallet, string memory uri) public onlyOwner {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(custodialWallet, tokenId);
        _setTokenURI(tokenId, uri);
        emit newNFTMinted(tokenId, custodialWallet);
    }
    // This function is used to set new NFT price if necessary
    function setNFTPrice(uint256 _newPrice) public onlyOwner {
        NFTPriceInUSDC = _newPrice;
        emit newPrice("New price is seted", _newPrice);
    }

    // Get token URI function
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }


    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

}