// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

contract CallerContract{
    uint public calledTimes = 0;

    function callFunctionDemo(address calleeContractAddress) public returns (bool success, bytes memory returnData) {
        // bytes memory payload = abi.encodeWithSignature("register(string)", "MyName");
        bytes memory payload = abi.encodeWithSignature("functionDemo()");
        (success, returnData) = calleeContractAddress.call(payload);
    }

    function delegateCallFunctionDemo(address calleeContractAddress) public returns (bool success, bytes memory returnData) {
        bytes memory payload = abi.encodeWithSignature("functionDemo()");
        (success, returnData) = calleeContractAddress.delegatecall(payload);
    }

    function staticCallGetCallTimes(address calleeContractAddress) public view returns (bool success, bytes memory returnData) {
        bytes memory payload = abi.encodeWithSignature("getCalledTimes()");
        (success, returnData) = calleeContractAddress.staticcall(payload);
    }

    function staticCallFunctionDemo(address calleeContractAddress) public view returns (bool success, bytes memory returnData) {
        bytes memory payload = abi.encodeWithSignature("functionDemo()");
        (success, returnData) = calleeContractAddress.staticcall(payload);
    }
}


contract CalleeContract{
    event FunctionCaller(address caller);

    uint public calledTimes = 10;

    function functionDemo() public returns (uint) {
        emit FunctionCaller(msg.sender);
        calledTimes++;
        return calledTimes;
    }

    function getCalledTimes() public view returns (uint) {
        return calledTimes;
    }
}
