// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;
import "@openzeppelin/contracts/utils/Strings.sol";
// import "bytes/BytesLib.sol";
import "solidity-bytes-utils/contracts/BytesLib.sol";

error Unauthorized(address ownerAddress, address callerAddress);
error Unauthorized1(address ownerAddress, bool temp, uint8[3] array);

contract ErrorHandlingDemo {
    event LogAddress(string addrStr, address addr);

    address owner;
    uint8 calledTimes = 0;

    constructor () {
        owner = msg.sender;
    }

    function assertFalse() public returns (uint8) {
        calledTimes++;
        assert(calledTimes == 1);
        return calledTimes;
    }

    function revertError() public returns (uint8) {
        // console.log("msg.sender = ", msg.sender);
        emit LogAddress("msg.sender = ", msg.sender);

        if (msg.sender != owner)
            revert Unauthorized(owner, msg.sender);

        calledTimes++;
        return calledTimes;
    }

    function revertError(address callerAddress) public returns (uint8) {
        emit LogAddress("callerAddress = ", callerAddress);

        if (callerAddress != owner)
            // revert Unauthorized(owner, callerAddress);
            revert Unauthorized1(owner, true, [1,2,3]);

        calledTimes++;
        return calledTimes;
    }

    function underflow(uint8 minuend, uint8 subtrahend) public returns (uint8 result) {
        result = minuend - subtrahend;
        calledTimes++;
        return result;
    }

    function overflow(uint8 firstAddend, uint8 secondAddend) public returns (uint8 result) {
        result = firstAddend + secondAddend;
        calledTimes++;
        return result;
    }

    function resetCalledTimes() public {
        delete calledTimes;
    }

    function getCalledTimes() public view returns (uint8) {
        return calledTimes;
    }

    function getCallerAddress() public view returns (address) {
        return msg.sender;
    }
}

contract ErrorHandlingCallerDemo {
    ErrorHandlingDemo errorHandlingDemo;

    constructor (address deployedContractAddress) {
        errorHandlingDemo = ErrorHandlingDemo(deployedContractAddress);
    }

    function assertFalse() public returns (string memory) {
        string memory returnString = "";
        uint8 calledTimes = 0;

        try errorHandlingDemo.assertFalse() returns (uint8) {
            calledTimes = errorHandlingDemo.getCalledTimes();
            returnString = string.concat("True: calledTimes = ", Strings.toString(calledTimes));
        } catch Panic(uint errorCode) {
            returnString = string.concat("False: errorCode = ", Strings.toString(errorCode));
        }

        return returnString;
    }

    function overflow(uint8 firstAddend, uint8 secondAddends) public returns (string memory) {
        string memory returnString = "";

        try errorHandlingDemo.overflow(firstAddend, secondAddends) returns (uint8 result) {
            returnString = string.concat("True: result = ", Strings.toString(result));
        } catch Panic(uint errorCode) {
            returnString = string.concat("False: errorCode = ", Strings.toString(errorCode));
        }

        return returnString;
    }

    function revertErrorWithEOAAddress() public returns (string memory returnString) {
        // string memory returnString = "";

        try errorHandlingDemo.revertError(msg.sender) returns (uint8 result) {
            returnString = string.concat("True: result = ", Strings.toString(result));
        } catch Error(string memory errReason) {
            returnString = string.concat("False: errReason = ", string(errReason));
        } catch (bytes memory customError) {
            bytes memory tempBytes = customError;
            bytes4 selector = bytes4(tempBytes);
            address owner;
            address callerAddress;

            if (selector == Unauthorized.selector) {
                owner = address(uint160(uint256(bytes32(BytesLib.slice(tempBytes, 4, 32)))));
                callerAddress = address(uint160(uint256(bytes32(BytesLib.slice(tempBytes, 36, 32)))));
                // (owner, eoaAddress) = abi.decode(tempBytes, (address, address));
                returnString = string.concat(
                    "Unauthorized: owner = ", 
                    Strings.toHexString(owner), 
                    // Strings.toHexString(uint256(uint160(owner)), 20), 
                    " callerAddress = ", 
                    Strings.toHexString(callerAddress)
                    );
            } else {
                returnString = "Other error";
            }
        }

        return returnString;
    }

    function revertError() public returns (string memory returnString) {

        try errorHandlingDemo.revertError() returns (uint8 result) {
            returnString = string.concat("True: result = ", Strings.toString(result));
        } catch Error(string memory errReason) {
            returnString = string.concat("False: errReason = ", string(errReason));
        // } catch Unauthorized(address ownerAddress, address eoaAddress) {
        //     returnString = string.concat(
        //         "Unauthorized: ownerAddress = ", Strings.toHexString(ownerAddress), 
        //         " eoaAddress = ", Strings.toHexString(eoaAddress)
        //         );
        } catch (bytes memory customError) {
            bytes memory tempBytes = customError;
            bytes4 selector = bytes4(tempBytes);
            address owner;
            address callerAddress;

            if (selector == Unauthorized.selector) {
                owner = address(uint160(uint256(bytes32(BytesLib.slice(tempBytes, 4, 32)))));
                callerAddress = address(uint160(uint256(bytes32(BytesLib.slice(tempBytes, 36, 32)))));
                // (owner, eoaAddress) = abi.decode(tempBytes, (address, address));
                returnString = string.concat(
                    "Unauthorized: owner = ", 
                    Strings.toHexString(owner), 
                    // Strings.toHexString(uint256(uint160(owner)), 20), 
                    " callerAddress = ", 
                    Strings.toHexString(callerAddress)
                    );
            } else {
                returnString = "Other error";
            }
        }

        return returnString;
    }

    function typeConvert() public pure returns (string memory returnString) {
        bytes4 expectedSelector = bytes4(Unauthorized.selector);
        bytes memory expectedSelectorBytes = abi.encodePacked(expectedSelector);
        string memory expectedSelectorString = string(expectedSelectorBytes);

        // returnString = string.concat(
        //     "False: expectedSelector = ", 
        //     expectedSelectorString
        //     );

        returnString = expectedSelectorString;
        return returnString;
        // return expectedSelectorBytes;
    }

    function getCallerAddress() public view returns (address, address) {
        address callerAddress = errorHandlingDemo.getCallerAddress();
        return (msg.sender, callerAddress);
    }
}
