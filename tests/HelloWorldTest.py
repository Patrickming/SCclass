import os

from ContractTest import ContractTest, Configuration


class HelloWorldTest(ContractTest):
    RETURN_STRING_FLAG_INDEX = 4

    def __init__(self):
        self.configuration = Configuration(os.path.basename(__file__))
        ContractTest.__init__(self, self.configuration)
        # Set the contract name to be test.
        self.contract_test_name = "HelloWorld"
        pass

    def init_test_result(self, test_result):
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

            # Method 2: call function directly
            returned_string = self.current_contract.functions.myFirstHelloWorld().call()
            # print("Debug: returned_string = " + str(returned_string))

            expected_string = "Hello World! My name is " + \
                              self.students.get_name_pinyin(self.current_student_index) + "."

            if returned_string == expected_string:
                return_value = True
                self.test_results[self.current_student_index][HelloWorldTest.RETURN_STRING_FLAG_INDEX] = 1
                print("Executed successfully.")
            else:
                print("\033[0;31;40mTest case failure: expected_string = " + expected_string + "\033[0m")
                print("\033[0;31;40m                   returned_string = " + returned_string + "\033[0m")
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return return_value

# python HelloWorldTest.py -c .\Configuration_201-1.json > test_result.txt
if __name__ == "__main__":
    contract_test = HelloWorldTest()
    contract_test.run()
