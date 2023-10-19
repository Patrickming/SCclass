import os
from time import sleep

from ContractTest import ContractTest, Configuration


class StringUtilTest(ContractTest):
    NULL_STRING_COMPARE_FLAG_INDEX = 4
    COMMON_STRING_COMPARE_FLAG_INDEX = 5

    def __init__(self):
        self.configuration = Configuration(os.path.basename(__file__))
        ContractTest.__init__(self, self.configuration)
        # Set the contract name to be test.
        self.contract_test_name = "StringUtilTest"
        pass

    def init_test_result(self, test_result):
        # NULL_STRING_COMPARE_FLAG_INDEX
        test_result.append(0)
        # COMMON_STRING_COMPARE_FLAG_INDEX
        test_result.append(0)
        pass

    # Implement its own test behaviours for HelloWorld.sol
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

            # sleep(10)
            # Method 2: call function directly
            returned_string1 = self.current_contract.functions.nullStringCompareTest().call()
            # print("Debug: returned_string = " + str(returned_string))

            returned_string2 = self.current_contract.functions.stringCompareTest().call()

            expected_string = "true"

            if returned_string1 == expected_string:
                return_value = True
                self.test_results[self.current_student_index][StringUtilTest.NULL_STRING_COMPARE_FLAG_INDEX] = 1
            else:
                print("\033[0;31;40mTest case failure: null string compare failed\033[0m")
                return_value = False

            if returned_string2 == expected_string:
                return_value = return_value and True
                self.test_results[self.current_student_index][StringUtilTest.COMMON_STRING_COMPARE_FLAG_INDEX] = 1
            else:
                print("\033[0;31;40mTest case failure: common string compare failed\033[0m")
                return_value = False

            if return_value:
                print("Executed successfully.")

        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return return_value

# python StringUtilTest.py -c .\Configuration_201-1.json > test_result.txt
if __name__ == "__main__":
    contract_test = StringUtilTest()
    contract_test.run()
