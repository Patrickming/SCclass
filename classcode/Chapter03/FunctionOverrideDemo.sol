// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract FirstBaseContract
{
    function baseFunction() virtual public {}
}

contract SecondBaseContract
{
    function amount() external view virtual returns(uint) { 
        return 10; 
    }

    function baseFunction() virtual public {}
    function baseFunction(uint) virtual public {}
}

contract DerivedContract is FirstBaseContract, SecondBaseContract
{
    uint public override amount;
    
    // Shall explicitly override the function with same name in all base contract.  
    function baseFunction() public override(FirstBaseContract, SecondBaseContract) {}
}