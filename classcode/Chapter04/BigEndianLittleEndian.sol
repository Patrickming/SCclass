// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

contract BigEndianLittleEndian{
	function operation(uint32 input) external pure returns (bytes1, bytes1){
        uint32 variable = 0x12345678;
        bytes4 temp1 = bytes4(input);
        bytes4 temp2 = bytes4(variable);
        return (temp1[0], temp2[0]);
	}
}