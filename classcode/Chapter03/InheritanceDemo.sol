// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

abstract contract GrandpaDemo {
    string myFamilyName;
    string myGivenName;

    constructor (string memory givenName, string memory familyName) {
        myFamilyName = familyName;
        myGivenName = givenName;
    }

    function getGivenName() public virtual view returns (string memory) {
        return myGivenName;
    }

    function getFamilyName() public view returns (string memory) {
        return myFamilyName;
    }
}

contract FatherDemo is GrandpaDemo {
    // state varible shadowing is not allowed
    // string myFamilyName;
    // string myGivenName;
    string myHouseAddress;

    constructor(string memory givenName, string memory familyName, string memory houseAddress) 
    GrandpaDemo(givenName, familyName)  {
        myHouseAddress = houseAddress;
    }

    function getGivenName() public virtual override view returns (string memory) {
        string memory answer = "Father's given name is ";
        string memory givenName = myGivenName;
        answer = string.concat(answer, givenName, ".");
        return answer;
    }

    function getHouseAddress() public view returns (string memory) {
        return myHouseAddress;
    }
}

// Joe, Biden, "1600 Pennsylvania Avenue NW, Washington, DC 20500.", USA001
contract ChildDemo is FatherDemo {
    // state varible shadowing is not allowed
    // string myFamilyName;
    // string myGivenName;
    // string myHouseAddress;
    string myCarLicense;

    constructor(string memory givenName, 
    string memory familyName, 
    string memory houseAddress,
    string memory carLicense) 
    FatherDemo(givenName, familyName, houseAddress)  {
        myCarLicense = carLicense;
    }

    function getGivenName() public override view returns (string memory) {
        string memory answer = "Child's given name is ";
        string memory givenName = GrandpaDemo.getGivenName();
        answer = string.concat(super.getGivenName(), " ", answer, givenName, ".");
        return answer;
    }

    // function shadowing is not allowed.
    // function getHouseAddress() public view returns (string memory) {
    //     return myHouseAddress;
    // }

    function getCarLicense() public view returns (string memory) {
        return myCarLicense;
    }
}
