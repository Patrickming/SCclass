// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract DeleteDemo {
    bytes bytesVarible = hex'00112233aabb';

    bytes bytesReference = bytesVarible;

    function deleteInteger() public pure returns (uint8) {
        uint8 tempInteger = 5;
        delete tempInteger;
        return tempInteger;
    }

    function deleteAddress() public pure returns (address) {
        address tempAddress = 0xdCad3a6d3569DF655070DEd06cb7A1b2Ccd1D3AF;
        delete tempAddress;
        return tempAddress;
    }

    function deleteReference() public returns (bytes memory, bytes memory, bytes memory) {
        bytes memory bytesVaribleMemory1 = bytesVarible;
        delete bytesReference;
        bytes memory bytesVaribleMemory2 = bytesVarible;
        delete bytesVarible;
        bytes memory bytesVaribleMemory3 = bytesVarible;
        return (bytesVaribleMemory1, bytesVaribleMemory2, bytesVaribleMemory3);
    }
}