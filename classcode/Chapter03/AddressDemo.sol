// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

// What are the return value of addressDemoOne and addressDemoTwo
// with parameter 0x00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff?
contract AddressDemo {
    address initAddress = 0x00112233445566778899AABbCCdDeeFf00112233;

    function addressDemoOne(bytes32 data) public pure returns (address) {
        address addressConverted = address(bytes20(data));
        return addressConverted;
    }

    function addressDemoTwo(bytes32 data) public pure returns (address) {
        address addressConverted = address(uint160(uint256(data)));
        return addressConverted;
    }
}
