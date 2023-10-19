import os
import random
from abc import abstractmethod

from typing import Tuple
from web3 import Web3

from ContractTest import ContractTest, Configuration


# TODO:编写实例就直接把这个TestAbstract里面的abstractmethod重写一下 demo在下面的类中体现(以32位转地址为例)
class TestAbstract(ContractTest):
    RETURN_STRING_FLAG_INDEX = 4

    def __init__(self):
        self.configuration = Configuration(os.path.basename(__file__))
        ContractTest.__init__(self, self.configuration)
        # Set the contract name to be test.
        self.contract_test_name = "AddressDemo"
        pass

    def init_test_result(self, test_result):
        test_result.append(0)
        pass

    @abstractmethod
    def judge(self) -> Tuple[bool, object, object]:
        pass

    # Implement its own test behaviours for AddressDemo.sol
    def execute(self):
        print("Executing test case.")
        return_value = False

        # Call
        try:
            # Method 1: send raw transaction
            # transaction = self.current_contract.functions.myFirstHelloWorld().buildTransaction({
            #     # "chainId": chain_id,
            #     "from": self.account_address_private_key[0][0],
            #     # "gasPrice": w3.eth.gas_price,
            #     "nonce": nonce
            # })
            # sign_transaction = self.web3.eth.account.sign_transaction(
            #     transaction, private_key=self.account_address_private_key[0][1]
            # )
            # transaction_hash = self.web3.eth.send_raw_transaction(sign_transaction.rawTransaction)
            # transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)

            # Method 2: call function directly

            # byte32_hex_str = random_hex_str()
            # bytes32_value, expected_string = StringUtilToByte32(byte32_hex_str)
            # # 调用合约函数并传递参数
            # returned_string = self.current_contract.functions.addressDemo(bytes32_value).call()
            # returned_string = "0x" + bytes.fromhex(returned_string[2:]).hex()
            # print("Debug: returned_string = " + str(returned_string))
            # print("Debug: expected_string = " + str(expected_string))
            res, returned_string, expected_string = self.judge()

            # 貌似在solidity中address类型返回到Python的类型是Str,没办法转化为String
            print("retrunstr:", returned_string)
            if res:
                return_value = True
                self.test_results[self.current_student_index][TestAbstract.RETURN_STRING_FLAG_INDEX] = 1
                print("Executed successfully.")
            else:
                print("\033[0;31;40mTest case failure: expected_string = " + expected_string + "\033[0m")
                print("\033[0;31;40m                   returned_string = " + returned_string + "\033[0m")
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return return_value


def random_hex_str() -> str:
    hex_chars = "0123456789ABCDEFabcdef"
    hex_string = ""

    for _ in range(64):
        # 生成一个随机的十六进制字符
        hex_char = random.choice(hex_chars)
        # 随机选择字符的大小写形式
        hex_char = random.choice([hex_char.upper(), hex_char.lower()])
        hex_string += hex_char

    return "0x" + hex_string


def StringUtilToByte32(hex_string: str) -> (bytes, str):
    #
    """
    :rtype: bytes,str
    """
    parameter = Web3.toBytes(hexstr=hex_string)
    bytes32_value = parameter.rjust(32, b"\x00")

    byte_array = bytes.fromhex(hex_string[2:])
    # 截取前20个字节
    excepted_result = byte_array[:20]

    # 截取前20个字节
    excepted_result = excepted_result.hex()
    return bytes32_value, "0x" + excepted_result

################### D E M O #########################################
class test_temp(TestAbstract):
    def judge(self) -> Tuple[bool, object, object]:
        byte32_hex_str = random_hex_str()
        bytes32_value, expected_string = StringUtilToByte32(byte32_hex_str)
        # 调用合约函数并传递参数
        returned_string = self.current_contract.functions.addressDemo(bytes32_value).call()
        returned_string = "0x" + bytes.fromhex(returned_string[2:]).hex()
        return returned_string == expected_string, returned_string, expected_string


if __name__ == '__main__':
    contract_test = test_temp()
    contract_test.run()
