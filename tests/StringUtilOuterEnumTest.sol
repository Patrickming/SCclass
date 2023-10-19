// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

import "./StringUtil.sol";

contract StringUtilTest {
    function nullStringCompareTest() public pure returns (string memory result){
        string memory str1;
        string memory str2;
        string memory str3 = "test";

        if (StringUtil.compare(str1, str2) != CompareResult.Invalid) {
            result = "false";
        }
        else if (StringUtil.compare(str1, str3) != CompareResult.Invalid) {
            result = "false";
        }
        else if (StringUtil.compare(str3, str1) != CompareResult.Invalid) {
            result = "false";
        }
        else {
            result = "true";
        }
    }

    function stringCompareTest() public pure returns (string memory result){
        string memory str1 = "test";
        string memory str2 = "testtest";
        string memory str3 = "tes";
        string memory str4 = "test";

        if (StringUtil.compare(str4, str1) != CompareResult.Equal) {
            result = "false";
        }
        else if (StringUtil.compare(str1, str4) != CompareResult.Equal) {
            result = "false";
        }
        else if (StringUtil.compare(str1, str2) != CompareResult.Less) {
            result = "false";
        }
        else if (StringUtil.compare(str2, str1) != CompareResult.Greater) {
            result = "false";
        }
        else if (StringUtil.compare(str1, str3) != CompareResult.Greater) {
            result = "false";
        }
        else if (StringUtil.compare(str3, str1) != CompareResult.Less) {
            result = "false";
        }
        else {
            result = "true";
        }
    }
}
