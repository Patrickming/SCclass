// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract AddressDemo {
    address initAddress = 0x00112233445566778899AABbCCdDeeFf00112233;
    //截取bytes32类型的低20字节后，再转换为地址类型返回。
    function addressDemo(bytes32 data) public pure returns (address) {
         return address(bytes20(data));
    }
}