// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract InitialDefaultValueDemo {
    enum Suit { Spades, Clubs, Diamonds, Hearts}

    bool boolVariable;
    uint uintVariable;
    int intVariable;
    bytes5 bytes5Variable;
    Suit enumVariable;
    bytes bytesVariable;
    string stringVariable;
    uint[5] arrayVariable;

    function getBoolDefaultValue() public view returns (bool){
        return boolVariable;
    }

    function getUnitDefaultValue() public view returns (uint){
        return uintVariable;
    }

    function getIntDefaultValue() public view returns (int){
        return intVariable;
    }

    function getBytes5DefaultValue() public view returns (bytes5){
        return bytes5Variable;
    }

    function getEnumDefaultValue() public view returns (Suit){
        return enumVariable;
    }

    function getBytesDefaultValue() public view returns (bytes memory){
        return bytesVariable;
    }

    function getStringDefaultValue() public view returns (string memory){
        return stringVariable;
    }

    function getArrayDefaultValue() public view returns (uint[5] memory){
        return arrayVariable;
    }
}
