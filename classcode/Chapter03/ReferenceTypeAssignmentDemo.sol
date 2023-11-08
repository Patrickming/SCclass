// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract ReferenceTypeAssignmentDemo {
    uint[5] arrayVariable = [10,20,30,40,50];

    function referenceTypeAssignmentDemo() public returns (uint, uint){
        memoryArrayAssignment(arrayVariable);
        storageArrayAssignment(arrayVariable);
        return (arrayVariable[3], arrayVariable[4]);
    }

    function memoryArrayAssignment(uint[5] memory inputArray) internal pure {
        inputArray[3] = 8;
    }

    function storageArrayAssignment(uint[5] storage inputArray) internal {
        inputArray[4] = 10;
    }
}
