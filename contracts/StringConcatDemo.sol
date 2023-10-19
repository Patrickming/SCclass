// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract StringConcatDemo {
    string myAgeStr;

    constructor() {
        myAgeStr = "My age is ";
    }

    function myAge(uint age) public view returns (string memory) {
        // 将myAgeStr转换为字节Str
        bytes memory Str = bytes(myAgeStr);
        // 创建一个新的字节数组Age，长度为3 最大年龄不超过999
        bytes memory Age = new bytes(3);

        
        // len用于存储age的位数
        uint len;
        // temp用于计算age的位数
        uint temp = age;
        for(len=0; temp != 0; len++) {
            temp /= 10;
        }

        // 如果age为0，则len为1
        if(age == 0) len = 1;

        // 根据age的位数生成对应的字节
        for(uint i=0; i < len; i++) {
            /*1. age / (10 ** (len - i - 1))取出相应位数的值 比如12岁 第一轮就是1 第二轮就是2
              2. uint8(... + 48) 转化为相应数字的ASCII码 0为48 所以加48
              3. bytes1(...) 将ASCII码转换为一个字节（字符）
            */
            Age[i] = bytes1(uint8(age / (10 ** (len - i - 1)) + 48));
            //移除年龄的第i+1位数字。例如：age是123时，那么当i为0时，age变为23 以此类推
            age %= 10 ** (len - i - 1);
        }

        // 后面返回的字节数组resultStr，长度为Str的长度加上len+1(结尾句号)
        bytes memory resultStr = new bytes(Str.length + len + 1);
        uint k = 0;
        // 将Str和Age的字节依次复制到resultStr中
        for (uint i = 0; i < Str.length; i++){
            resultStr[k++] = Str[i];
        } 
        for (uint i = 0; i < len; i++) {
            resultStr[k++] = Age[i];
        }
        // 在结果字符串的末尾添加一个点
        resultStr[k++] = bytes1(uint8(46));

        return string(resultStr);
    }
}
