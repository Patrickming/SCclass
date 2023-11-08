// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract BytesNDemo {
    bytes4 bytesVaraibleOne;
    bytes4 bytesVaraibleTwo;

    constructor () {
        // '0' equals to 0x30
        bytesVaraibleOne = '01';
        // 'a' equals to 0x61
        bytesVaraibleTwo = 'ab';
    }

    function bytesBitAnd() public view returns (bytes4){
        bytes4 returnValue = bytesVaraibleOne & bytesVaraibleTwo;
        return returnValue;
    }

    function bytesBitOr() public view returns (bytes4){
        bytes4 returnValue = bytesVaraibleOne | bytesVaraibleTwo;
        return returnValue;
    }

    function bytesBitLeftShift(uint8 shiftTimes) public view returns (bytes4){
        bytes4 returnValue = bytesVaraibleOne << shiftTimes;
        return returnValue;
    }

    function bytesElementFetch(uint8 index) public view returns (bytes4){
        bytes4 returnValue = bytesVaraibleTwo[index];
        return returnValue;
    }
}

