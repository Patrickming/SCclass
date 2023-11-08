// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

abstract contract BaseContract {
    uint varaible;
    constructor(uint param) { varaible = param; }
}

contract DerivedFirstContract is BaseContract(5) {
    constructor() {}
}

contract DerivedSecondContract is BaseContract {
    constructor(uint y) BaseContract(y * 2) {}
}

abstract contract DerivedThirdContract is BaseContract {
}

contract DerivedFourthContract is DerivedThirdContract {
    constructor() BaseContract(2 + 2) {}
}