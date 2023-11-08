// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract Crowd {
    uint public fundingGoal = 2 ether;
    uint public totalDonateValue = 0;
    uint public donateCount = 0;
    
    constructor() {}

    fallback () external {}

    function donate() public payable {
        uint256 value = msg.value;

        if (value > 0) {
            totalDonateValue = totalDonateValue + value;
            donateCount++;
        }
    }
}