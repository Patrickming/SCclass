// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;
import "./StringUtil.sol";

contract HelloWorld {
    function myFirstHelloWorld() public virtual pure returns (string memory) {
        return "Hello World! My name is Xia Ruoming.";
    }
}

contract HelloMyWorld is HelloWorld {

    function myFirstHelloWorld() public override pure returns (string memory) {
        string memory myString = super.myFirstHelloWorld();
        if (StringUtil.compare("Hello World! My name is Zhang San.",myString) == StringUtil.CompareResult.Equal) {
            return "It's not me!";
        } else {
            return string(abi.encodePacked(myString, " My class number is 214."));
        }
    }
}
