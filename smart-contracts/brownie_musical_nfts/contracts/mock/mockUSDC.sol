// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/access/Ownable.sol";

contract MockUSDC is ERC20, Ownable {
    constructor(uint256 _intialSuppplay) ERC20("MockUSDC", "MUSDC") {
        // Mint to deoployer all MUSDC tokens
        _mint(msg.sender, _intialSuppplay * 10 ** decimals());
    }
}