// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract Crowd {
    uint public fundingGoal = 2 ether;
    uint public totalDonateValue;
    uint public specialDonateValue = 2021131135;
    uint public donateCount;
    address public beneficiary;

    constructor (address beneficiaryInput) {
        require(beneficiaryInput != msg.sender);
        beneficiary = beneficiaryInput;
    }

    modifier onlyBeneficiary() {
        require(msg.sender == beneficiary, "Only beneficiary can call this.");
        _;
    }

    function donate() public payable {
        totalDonateValue += msg.value;
        donateCount += 1;
        require(totalDonateValue <= fundingGoal, "Total donates exceeds the funding goal.");
    }

    function specialDonate() public payable {
        require(msg.value == specialDonateValue, "Donate value is not correct, it should be 2021131135 wei.");
        totalDonateValue += msg.value;
        donateCount += 1;
        require(totalDonateValue <= fundingGoal, "Total donates exceeds the funding goal.");
    }

    function withdraw(uint value) public payable onlyBeneficiary {
        require(address(this).balance >= totalDonateValue, "The balance is not enough.");
        totalDonateValue -= value;
        payable(beneficiary).transfer(totalDonateValue);
    }
}
