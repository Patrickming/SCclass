// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

import "@openzeppelin/contracts/utils/Strings.sol";

contract EncodeDemo{
    event MsgCallData(bytes callData);
    struct Test{
        uint16 member1;
        bytes member2;
        string member3;
    }

    function boolDemo(bool boolParam) external pure returns (string memory returnStr){
        returnStr = boolParam ? "True" : "False";
    }

	function functionDemo(
        uint160 firstParam, 
        bool secondParam) 
        external returns (
            string memory returnString){
        emit MsgCallData(msg.data);

        returnString = string.concat(
            "firstParam = ",
            Strings.toString(firstParam),
            " secondParam = ",
            secondParam ? "True" : "False"
        );
	}

    // 10,[10,20,30],true,0x414243
	function functionDynamicDemo(
        uint160 firstParam, 
        uint32[] memory secondParam, 
        bool thirdParam,
        bytes memory fourthParam) 
        public returns(
            string memory returnString){
        emit MsgCallData(msg.data);

        returnString = string.concat(
            "firstParam = ",
            Strings.toString(firstParam),
            " secondParam.length = ",
            Strings.toString(secondParam.length),
            " thirdParam = ",
            thirdParam ? "True" : "False",
            " fourthParam.length = ",
            Strings.toString(fourthParam.length)
        );
	}

    function getFunction() external view 
    returns(function (uint160,bool) external returns (string memory)) {
        return this.functionDemo;
    }

    function getFunctionSelector() external pure 
    returns(bytes4) {
        return this.functionDemo.selector;
    }
}

contract Caller {
    address calleeContractAddress;
    function (uint160,bool) external returns (string memory) functionVaraible;

    constructor(address callee){
        calleeContractAddress = callee;
    }

    function functionCall(function (uint160,bool) external returns (string memory) func) public returns(bytes memory, string memory){
        return (msg.data, func(1, false));
    }

    function delegateCallDemo() public returns (bool success, bytes memory returnData) {
        bytes memory payload = abi.encodeWithSignature("getFunction()");
        (success, returnData) = calleeContractAddress.delegatecall(payload);
    }

    function functionTypeCall() external returns (bytes memory, string memory) {
        return this.functionCall(EncodeDemo(calleeContractAddress).functionDemo);
    }
}
