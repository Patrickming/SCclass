// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

/**
* CopyRright (c)2023 - 2023: CUIT
* Project: 
* Comments:
* Author: Water Wang
* Create Date: 2022-09-25
* Modified By: Water Wang
* Modified Date: 2023-09-14
* 
*/
contract StrongTypeDemo{
    string myAgeStr = 'My age is ';

    //constructor function with default value
    constructor () {
    }

    /*
     * FunName: myAge
     * Description: returns a string like 'My age is 10.' according to input age number
     * @param: age
     * @return string memory: a string like 'My age is 10.'
     * the age number comes from the input parameter of this function
     * @Author: Water Wang
     * @Create Date: 2023-09-14
    */
 	function myAge(uint age) public view returns (string memory){
        // string memory tempValue = myAgeStr + age;
        string memory tempAgeStr;

        if (age == 0) tempAgeStr = '0.';
        else {
            while (age != 0) {
                uint remainder = age % 10;
                age = age / 10;
                tempAgeStr = strConcat(uintToStr(remainder), tempAgeStr);
            }

            tempAgeStr = strConcat(tempAgeStr, '.');
        }

        string memory returnValue = strConcat(myAgeStr, tempAgeStr);
		return	returnValue;
	}

    function strConcat(string memory str1, string memory str2) internal pure returns (string memory){
        bytes memory strBytes1 = bytes(str1);
        bytes memory strBytes2 = bytes(str2);
        string memory returnStr = new string(strBytes1.length + strBytes2.length);
        bytes memory returnBytes = bytes(returnStr);

        uint k = 0;
        uint i = 0;
        for (i = 0; i < strBytes1.length; i++) returnBytes[k++] = strBytes1[i];
        for (i = 0; i < strBytes2.length; i++) returnBytes[k++] = strBytes2[i];
        
        return string(returnBytes);
   }

    function uintToStr(uint256 value) internal pure returns(string memory) {
        bytes memory alphabet = "0123456789abcdef";
        bytes memory data = abi.encodePacked(value);
        bytes memory str = new bytes(1);
        uint i = data.length - 1;

        str[0] = alphabet[uint(uint8(data[i] & 0x0f))];

        return string(str);
    }
}