// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.16;
pragma abicoder v2;


contract Test1 {
    constructor() { b = hex"12345678901234567890123456789012"; }
    event Event(uint indexed a, bytes32 b);
    event Event2(uint a, bytes32 b);
    error InsufficientBalance(uint256 available, uint256 required);
    function foo(uint a) public {
        emit Event(a, b);
        emit Event2(a + 1, b);
    }
    bytes32 b;
}

contract Test2 {
    struct S { uint a; uint[] b; T[] c; }
    struct T { uint x; uint y; }
    function f(S memory, T memory, uint) public pure {}
    function g() public pure returns (S memory, T memory, uint) {}
}

