import os

from ContractTest import ContractTest, Configuration
from StudentsList import Students


class HelloMyWorldTest(ContractTest):
    FOR_NOT_USED_FLAG_INDEX = 4
    COMPARE_USED_FLAG_INDEX = 5
    ZHANG_SAN_USED_FLAG_INDEX = 6
    CONCAT_USED_FLAG_INDEX = 7
    RETURN_STRING_FLAG_INDEX = 8

    def __init__(self):
        configuration = Configuration(os.path.basename(__file__))
        ContractTest.__init__(self, configuration=configuration)
        # Set the contract name to be test.
        self.contract_test_name = "HelloMyWorld"
        self.solidity_file = None
        pass

    def init_test_result(self, test_result):
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        pass

    def open_solidity_file(self):
        self.solidity_file = open(
            self.config.configuration[Configuration.SOLIDITY_FILES][0][Configuration.FILE_NAME],
            "r"
        )

    def close_solidity_file(self):
        self.solidity_file.close()

    def check_grammar(self):
        result = True
        for_used = False
        string_util_compare_used = False
        zhang_san_used = False
        string_concat_used = False
        encode_packed_used = False

        lines = self.solidity_file.readlines()

        for line in lines:
            if 'for' in line and 'using' not in line:
                for_used = True

            if 'StringUtil.compare' in line:
                string_util_compare_used = True

            if 'Zhang San.' in line:
                zhang_san_used = True

            if 'string.concat' in line:
                string_concat_used = True

            if 'abi.encodePacked' in line and 'string' in line:
                encode_packed_used = True

        if for_used:
            print("\033[0;31;40mTest case failure: Shall not use for loop\033[0m")
        else:
            self.test_results[self.current_student_index][HelloMyWorldTest.FOR_NOT_USED_FLAG_INDEX] = 1

        if not string_util_compare_used:
            print("\033[0;31;40mTest case failure: Shall use StringUtil.compare to compare string\033[0m")
        else:
            self.test_results[self.current_student_index][HelloMyWorldTest.COMPARE_USED_FLAG_INDEX] = 1

        if not zhang_san_used:
            print("\033[0;31;40mTest case failure: Shall compare with 'Zhang San.'\033[0m")
        else:
            self.test_results[self.current_student_index][HelloMyWorldTest.ZHANG_SAN_USED_FLAG_INDEX] = 1


        if (not string_concat_used) and (not encode_packed_used):
            print("\033[0;31;40mTest case failure: "
                  "Shall use string.concat or abi.encodePacked to concat string.'\033[0m")
        else:
            self.test_results[self.current_student_index][HelloMyWorldTest.CONCAT_USED_FLAG_INDEX] = 1

        result = (not for_used) and string_util_compare_used and \
                 string_util_compare_used and zhang_san_used and \
                 (string_concat_used or encode_packed_used)

        return result

    # Implement its own test behaviours for HelloWorld.sol
    def execute(self):
        print("Executing test case.")
        return_value = True

        # Call 
        try:
            self.open_solidity_file()
            return_value = self.check_grammar()

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
            # TODO: self.current_contract is the last deployed contract, need to be optimize.
            self.web3.eth.handleRevert = True
            returned_string = self.current_contract.functions.myFirstHelloWorld().call()
            # print("Debug: returned_string = " + str(returned_string))

            expected_string = "Hello World! My name is " + \
                              self.students.get_name_pinyin(self.current_student_index) + "." + \
                              " My class number is " + \
                              self.students.students_list[self.current_student_index][
                                  Students.STUDENT_CLASS_NUMBER_INDEX] + \
                              "."

            if returned_string != expected_string:
                print("\033[0;31;40mTest case failure: expected_string = " + expected_string + "\033[0m")
                print("\033[0;31;40m                   returned_string = " + returned_string + "\033[0m")
                return_value = False

            if return_value:
                self.test_results[self.current_student_index][HelloMyWorldTest.RETURN_STRING_FLAG_INDEX] = 1
                print("Executed successfully.")

            self.close_solidity_file()
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")
            return_value = False

        return return_value


# python HelloMyWorldTest.py -c .\Configuration_201-1.json > test_result.txt
if __name__ == "__main__":
    contract_test = HelloMyWorldTest()
    contract_test.run()
