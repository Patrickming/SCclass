// SPDX-License-Identifier: MIT

pragma solidity ^0.8.16;

library StringUtil {
    //1、库中定义枚举类型CompareResult，成员为Equal、Less、Greater、Invalid
    enum CompareResult { Equal, Less, Greater, Invalid }
    //字符串比较函数
    function compare(string memory str1, string memory str2) public pure returns (CompareResult) {
        bytes memory bStr1 = bytes(str1);
        bytes memory bStr2 = bytes(str2);
        //输入参数字符串str1、字符串str2任意一个参数是空字符串 返回Invalid
        if(bStr1.length == 0 || bStr2.length == 0) {
            return CompareResult.Invalid;
        }
        //算出
        uint minLength = bStr1.length;
        if(bStr2.length < minLength) {
            minLength = bStr2.length;
        }
        //str1的字符ascii码值 小于/大于 str2对应位置的字符ascii码值 返回Less or Greater
        //str1与str2[0, str1.length]或str2与str1[0, str2.length]字符串内容相同则跳过
        for(uint i = 0; i < minLength; i ++) {
            if(bStr1[i] < bStr2[i]) {
                return CompareResult.Less;
            } else if(bStr1[i] > bStr2[i]) {
                return CompareResult.Greater;
            }
        }
        //str1的长度 小于/大于 str2的长度 返回Less or Greater
        if(bStr1.length < bStr2.length) {
            return CompareResult.Less;
        } else if(bStr1.length > bStr2.length) {
            return CompareResult.Greater;
        } else {
            return CompareResult.Equal;
        }
    }
}
