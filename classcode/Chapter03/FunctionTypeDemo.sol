// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract FunctionTypeDemo {
    enum MessageData {Initiate, Processing, Finished}
    enum MessageResponse {Success, Failure}

    struct Message {
        MessageData messageData;
        function(MessageResponse) external messageCallback;
    }

    Message[] private messages;
    event MessageLength(uint);

    function notify(MessageData messageData, function(MessageResponse) external messageCallback) public {
        messages.push(Message(messageData, messageCallback));
        emit MessageLength(messages.length);
    }

    // Is there any bug in function response
    function response(MessageResponse responseData) private  {
        messages[0].messageCallback(responseData);
        messages.pop();
    }

    function handleMessage() public {
        emit MessageLength(messages.length);

        if (messages.length > 0) {
            if (messages[0].messageData == MessageData.Initiate) {
                // Do something related to received message
                response(MessageResponse.Success);
            }
            else if (messages[0].messageData == MessageData.Processing) {
                // Do something related to received message
                response(MessageResponse.Success);
            }
            else if (messages[0].messageData == MessageData.Finished) {
                // Do something related to received message
                response(MessageResponse.Failure);
            }
        }

        emit MessageLength(messages.length);
    }
}


contract FunctionTypeUser {
    event NewResponse(FunctionTypeDemo.MessageResponse);

    FunctionTypeDemo private contractNotified;
    FunctionTypeDemo.MessageResponse private dataReceived;

    constructor (address functionTypeDemo) {
        contractNotified = FunctionTypeDemo(functionTypeDemo);
    }

    function notifiy(FunctionTypeDemo.MessageData notifiedData) public {
        contractNotified.notify(notifiedData, this.response);
    }

    function response(FunctionTypeDemo.MessageResponse responseData) external {
        require(
            msg.sender == address(contractNotified),
            "Only FunctionTypeDemo can call this."
        );
        dataReceived = responseData;
        emit NewResponse(responseData);
    }
}