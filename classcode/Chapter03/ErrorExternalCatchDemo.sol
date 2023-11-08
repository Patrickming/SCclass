// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

contract Callee {
    function func() public pure returns (bool) {assert(false);return true;}
}

contract Caller {
    Callee callee = new Callee();
    function func() public pure returns (bool) {revert("intent revert");}

    function catchExternal() public view returns (uint result) {
        try callee.func() {
            result = 0;
            this.func();
        } catch Panic(uint errorCode) {
            result = errorCode;
        } catch Error(string memory reason) {
            result = 0xff;
        }
    }

    // function catchInternal() public view returns (uint result) {
    //     try func() {
    //         result = 0;
    //         this.func();
    //     } catch Panic(uint errorCode) {
    //         result = errorCode;
    //     } catch Error(string memory reason) {
    //         result = 0xff;
    //     }
    // }
}