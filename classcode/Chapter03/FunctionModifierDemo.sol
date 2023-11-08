// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract FunctionModifierDemo {
    address public owner;

    constructor () {
        owner = msg.sender;
    }

    modifier onlyOwner {
        _;
        require(msg.sender == owner);
    }

    function transferOwnership(address newOwner) public onlyOwner {
        owner = newOwner;
    }
}
