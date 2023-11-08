// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract A {
    uint variableA = 10;
    function a() virtual external view returns (uint) {return variableA;}
    function a(uint param) virtual public view returns (uint) {return variableA + param;}
    function b() public pure returns (uint) {return 2;}
    // function c() virtual private view returns (uint) {return variable;}
    function d() private view returns (uint) {return variableA + 10;}
}
contract B is A {
    uint variableB = 20;
    function a() virtual override public view returns (uint) {
        uint temp = 3;
        uint variable = super.a(temp);
        return variable + 3;
    }
    // function b() public pure returns (uint) {}
}
contract C is A {
    uint variableC = 30;
    function a() virtual override(A) public pure returns (uint) {return 4;}
    function c() external view virtual returns(uint) { return 3;}
}
contract D is A, B, C {
    uint variableD = 40;
    function a() override(A, B, C) public pure returns (uint) {return 5;}
}


contract E is A, C, B {
    uint variableE = 50;
    function a() override(A, B, C) public pure returns (uint) {return 6;}
    // external function C.c() has same parameter and return types 
    // as the getter function of state variable c,
    // state variable c can override external function C.c().
    uint public override c;
}
// Below contract F can not be compiled successfully
// contract F is B, A {}