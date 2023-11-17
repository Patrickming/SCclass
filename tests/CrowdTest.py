import os
import random
from typing import Tuple

from web3 import Web3

from ContractTest import ContractTest, Configuration


class CrowdTest(ContractTest):
    DONATE_OVER_1 = 4
    DONATE_ONE_ETHER = 5
    DONATE_CHECK_TOTAL_DONATE_1 = 6
    DONATE_CHECK_BALANCE_1 = 7
    DONATE_CHECK_DONATE_COUNT_1 = 8
    DONATE_STUDENT_NUMBER_WEI = 9
    DONATE_CHECK_TOTAL_DONATE_2 = 10
    DONATE_CHECK_BALANCE_2 = 11
    DONATE_CHECK_DONATE_COUNT_2 = 12
    DONATE_OVER_2 = 13

    SPECIAL_DONATE_OVER_1 = 14
    SPECIAL_DONATE_STUDENT_NUMBER_WEI = 15
    SPECIAL_DONATE_CHECK_TOTAL_DONATE = 16
    SPECIAL_DONATE_CHECK_BALANCE = 17
    SPECIAL_DONATE_CHECK_DONATE_COUNT = 18
    SPECIAL_DONATE_OVER_2 = 19

    WITHDRAW_NONE_BENEFICIARY = 20
    WITHDRAW_OVER = 21
    WITHDRAW_EQUAL = 22
    WITHDRAW_STUDENT_NUMBER_WEI = 23

    BENEFICIARY_ADDRESS_INDEX = 1
    DONATOR_ADDRESS_INDEX = 2
    NONE_BENEFICIARY_ADDRESS_INDEX = 3

    TOTAL_DONATES_EXCEEDS_FUNDING_GOAL = "Total donates exceeds the funding goal."
    DONATE_VALUE_IS_NOT_CORRECT = "Donate value is not correct, it should be "
    WEI = " wei."
    ONLY_BENEFICIARY_CAN_CALL = "Only beneficiary can call this."
    THE_BALANCE_IS_NOT_ENOUGH = "The balance is not enough."

    def __init__(self):
        self.configuration = Configuration(os.path.basename(__file__))
        ContractTest.__init__(self, self.configuration)
        # Set the contract name to be tested.
        self.contract_test_name = "Crowd"
        self.donate_count = 0
        self.expect_total_donate_value = 0
        pass

    def init_test_result(self, test_result):
        # DONATE_FLAG_INDEX
        test_result.append(0)
        # SPECIAL_DONATE_FLAG_INDEX
        test_result.append(0)
        # WITHDRAW_FLAG_INDEX
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        test_result.append(0)
        pass

    # 调用部署时候的constructor函数，向里面传递受益人的地址self.config.configuration[Configuration.ACCOUNTS][CrowdTest.BENEFICIARY_ADDRESS_INDEX][Configuration.ADDRESS]
    # 就是受益人的地址
    def construct_contract(self, nonce, eoa_index):
        ret = self.current_contract.constructor(
            self.config.configuration[Configuration.ACCOUNTS]
            [CrowdTest.BENEFICIARY_ADDRESS_INDEX][Configuration.ADDRESS]).buildTransaction(
            {
                # "chainId": chain_id,
                "gas": 30000000,
                "gasPrice": self.web3.eth.gas_price,
                "from": self.config.configuration[Configuration.ACCOUNTS][eoa_index][Configuration.ADDRESS],
                "nonce": nonce,
            }
        )

        return ret

    # 向donate函数转账的Python函数 number 转账的数量,uint 转账的单位: "wei" 或 "ether"
    def send_wei_to_contract_donate(self, number: int, uint: str, address: str):
        tx_hash = self.current_contract.functions.donate().transact(
            {'from': address, 'value': self.web3.toWei(number, uint)})
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)  # 收据:表示的是交易的详情，包含gas和转账金额
        # print(tx_receipt)
        wallet = self.web3.to_checksum_address(
            self.config.configuration[Configuration.ACCOUNTS][CrowdTest.DONATOR_ADDRESS_INDEX][
                Configuration.ADDRESS])
        # print(self.web3.eth.getBalance(wallet))
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def send_wei_to_special_contract_donate(self, number: int, uint: str, address: str):
        tx_hash = self.current_contract.functions.specialDonate().transact(
            {'from': address, 'value': self.web3.toWei(number, uint)})
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)  # 收据:表示的是交易的详情，包含gas和转账金额
        # print(tx_receipt)
        wallet = self.web3.to_checksum_address(
            self.config.configuration[Configuration.ACCOUNTS][CrowdTest.DONATOR_ADDRESS_INDEX][
                Configuration.ADDRESS])
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def withdraw(self, number: int, address: str):
        tx_hash = self.current_contract.functions.withdraw(number).transact(
            {'from': address})
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)  # 收据:表示的是交易的详情，包含gas和转账金额
        # print(tx_receipt)
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def donate_test(self):
        return_value = True
        participant_address = ""
        returned_error_message = ""

        try:
            # Donate 3 ether from participant address
            participant_address = self.config.configuration[Configuration.ACCOUNTS][CrowdTest.DONATOR_ADDRESS_INDEX][
                Configuration.ADDRESS]
            self.send_wei_to_contract_donate(3, "ether", participant_address)

            # Donate value exceed totalDonateValue
            return_value = False
            print(
                "\033[0;31;40mTest case donate_test donate 3 ether overflow failure:\n    expected_error_message = " +
                self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL):
                # if you find the TOTAL_DONATES_EXCEEDS_FUNDING_GOAL means the function is correct
                self.test_results[self.current_student_index][self.DONATE_OVER_1] = 1
                return_value = True
            else:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate 3 ether overflow failure:\n    "
                      "expected_error_message = " + self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL + "\033[0m")
                print("\033[0;31;40m    returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        try:
            initial_balance = self.web3.eth.getBalance(self.current_contract.address)

            # Donate 1 ether from participant address
            self.send_wei_to_contract_donate(1, "ether", participant_address)
            self.donate_count += 1

            # Check if the totalDonateValue has been updated correctly
            returned_total_donate_value = self.current_contract.functions.totalDonateValue().call()
            self.expect_total_donate_value = Web3.toWei(1, "ether")
            if returned_total_donate_value != self.expect_total_donate_value:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate 1 ether failure:\n    expected_total_donate_value = " +
                      str(self.expect_total_donate_value) + " wei\033[0m")
                print("\033[0;31;40m    returned_total_donate_value = " +
                      str(returned_total_donate_value) + " wei\033[0m")
            else:
                self.test_results[self.current_student_index][self.DONATE_CHECK_TOTAL_DONATE_1] = 1

            # Check if the contract balance has been updated correctly
            returned_contract_balance = self.web3.eth.getBalance(self.current_contract.address)
            expected_contract_balance = initial_balance + Web3.toWei(1, "ether")

            if returned_contract_balance != expected_contract_balance:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate 1 ether failure:\n    expected_contract_balance = " +
                      str(expected_contract_balance) + " ether\033[0m")
                print("\033[0;31;40m    returned_contract_balance = " +
                      str(returned_contract_balance) + " ether\033[0m")
            else:
                self.test_results[self.current_student_index][self.DONATE_CHECK_BALANCE_1] = 1

            # Check if the donateCount has been incremented correctly
            returned_donate_count = self.current_contract.functions.donateCount().call()
            expected_donate_count = self.donate_count
            if returned_donate_count != expected_donate_count:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate 1 ether failure:\n    expected_donate_count = " +
                      str(expected_donate_count) + "\033[0m")
                print("\033[0;31;40m    returned_donate_count = " +
                      str(returned_donate_count) + "\033[0m")
            else:
                self.test_results[self.current_student_index][self.DONATE_CHECK_DONATE_COUNT_1] = 1
                self.test_results[self.current_student_index][self.DONATE_ONE_ETHER] = 1

            # Donate 1 - studentNumber ether from participant address
            temp_value = 1000000000000000000 - \
                         int(self.students.students_list[self.current_student_index][self.students.STUDENT_NUMBER_INDEX])
            self.send_wei_to_contract_donate(temp_value, "wei", participant_address)
            self.donate_count += 1

            # Check if the totalDonateValue has been updated correctly
            returned_total_donate_value = self.current_contract.functions.totalDonateValue().call()
            self.expect_total_donate_value += temp_value
            if returned_total_donate_value != self.expect_total_donate_value:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate " + str(temp_value) +
                      " wei failure:\n    expected_total_donate_value = " +
                      str(self.expect_total_donate_value) + " wei\033[0m")
                print("\033[0;31;40m    returned_total_donate_value = " +
                      str(returned_total_donate_value) + " wei\033[0m")
            else:
                self.test_results[self.current_student_index][self.DONATE_CHECK_TOTAL_DONATE_2] = 1

            # Check if the contract balance has been updated correctly
            returned_contract_balance = self.web3.eth.getBalance(self.current_contract.address)
            expected_contract_balance = initial_balance + Web3.toWei(1, "ether") + temp_value
            if returned_contract_balance != expected_contract_balance:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate " + str(temp_value) +
                      " wei failure:\n    expected_beneficiary_balance = " +
                      str(expected_contract_balance) + " ether\033[0m")
                print("\033[0;31;40m    returned_beneficiary_balance = " +
                      str(returned_contract_balance) + " ether\033[0m")
            else:
                self.test_results[self.current_student_index][self.DONATE_CHECK_BALANCE_2] = 1

            # Check if the donateCount has been incremented correctly
            returned_donate_count = self.current_contract.functions.donateCount().call()
            expected_donate_count = self.donate_count
            if returned_donate_count != expected_donate_count:
                return_value = False
                print("\033[0;31;40mTest case donate_test donate " + str(temp_value) +
                      " wei failure:\n    expected_donate_count = " +
                      str(expected_donate_count) + "\033[0m")
                print("\033[0;31;40m    returned_donate_count = " +
                      str(returned_donate_count) + "\033[0m")
            else:
                self.test_results[self.current_student_index][self.DONATE_CHECK_DONATE_COUNT_2] = 1
                self.test_results[self.current_student_index][self.DONATE_STUDENT_NUMBER_WEI] = 1
        except Exception as e:
            print("\033[0;31;40mException donate_test donate 1 ether and student number wei:\n    "
                  + str(e) + "\033[0m")
            return_value = False

        try:
            # Donate 1 ether from participant address
            participant_address = self.config.configuration[Configuration.ACCOUNTS][CrowdTest.DONATOR_ADDRESS_INDEX][
                Configuration.ADDRESS]
            self.send_wei_to_contract_donate(1, "ether", participant_address)

            # Donate value exceed totalDonateValue
            return_value = False
            print(
                "\033[0;31;40mTest case donate_test donate 1 ether overflow failure:\n    expected_error_message = " +
                self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL):
                # if you find the TOTAL_DONATES_EXCEEDS_FUNDING_GOAL means the function is correct
                return_value = True
                self.test_results[self.current_student_index][self.DONATE_OVER_2] = 1
            else:
                return_value = False
                print("\033[0;31;40mTest case donate_test failure: expected_error_message = " +
                      self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL + "\033[0m")
                print("\033[0;31;40m                               returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        return return_value

    def special_donate_test(self):
        return_value = True
        participant_address = ""
        returned_error_message = ""
        expected_error_message = ""
        try:
            # Donate 3 ether from participant address
            participant_address = self.config.configuration[Configuration.ACCOUNTS][CrowdTest.DONATOR_ADDRESS_INDEX][
                Configuration.ADDRESS]
            expected_error_message = \
                self.DONATE_VALUE_IS_NOT_CORRECT + \
                self.students.students_list[self.current_student_index][self.students.STUDENT_NUMBER_INDEX] + \
                self.WEI
            self.send_wei_to_special_contract_donate(3, "ether", participant_address)

            # Donate value exceed totalDonateValue
            return_value = False
            print(
                "\033[0;31;40mTest case special_donate_test not special donate failure:\n    "
                "expected_error_message = " + expected_error_message + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(expected_error_message):
                # if you find the same code means the function is correct
                self.test_results[self.current_student_index][self.SPECIAL_DONATE_OVER_1] = 1
                return_value = True
            else:
                return_value = False
                print("\033[0;31;40mTest case special_donate_test not special donate failure:\n    "
                      "expected_error_message = " + expected_error_message + "\033[0m")
                print("\033[0;31;40m    returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        try:
            initial_balance = self.web3.eth.getBalance(self.current_contract.address)

            # Donate studentNumber wei from participant address
            temp_value = int(self.students.students_list[self.current_student_index][self.students.STUDENT_NUMBER_INDEX])
            self.send_wei_to_contract_donate(temp_value, "wei", participant_address)
            self.donate_count += 1

            # Check if the totalDonateValue has been updated correctly
            returned_total_donate_value = self.current_contract.functions.totalDonateValue().call()
            self.expect_total_donate_value += temp_value
            if returned_total_donate_value != self.expect_total_donate_value:
                return_value = False
                print("\033[0;31;40mTest case special_donate_test " + str(temp_value) +
                      " wei failure:\n    expected_total_donate_value = " +
                      str(self.expect_total_donate_value) + " wei\033[0m")
                print("\033[0;31;40m    returned_total_donate_value = " +
                      str(returned_total_donate_value) + " wei\033[0m")
            else:
                self.test_results[self.current_student_index][self.SPECIAL_DONATE_CHECK_TOTAL_DONATE] = 1


            # Check if the contract balance has been updated correctly
            returned_contract_balance = self.web3.eth.getBalance(self.current_contract.address)
            expected_contract_balance = initial_balance + temp_value

            if returned_contract_balance != expected_contract_balance:
                return_value = False
                print("\033[0;31;40mTest case special_donate_test " + str(temp_value) +
                      " wei failure:\n    expected_beneficiary_balance = " +
                      str(expected_contract_balance) + " ether\033[0m")
                print("\033[0;31;40m    returned_beneficiary_balance = " +
                      str(returned_contract_balance) + " ether\033[0m")
            else:
                self.test_results[self.current_student_index][self.SPECIAL_DONATE_CHECK_BALANCE] = 1


            # Check if the donateCount has been incremented correctly
            returned_donate_count = self.current_contract.functions.donateCount().call()
            expected_donate_count = self.donate_count
            if returned_donate_count != expected_donate_count:
                return_value = False
                print("\033[0;31;40mTest case special_donate_test " + str(temp_value) +
                      " wei failure:\n    expected_donate_count = " +
                      str(expected_donate_count) + "\033[0m")
                print("\033[0;31;40m    returned_donate_count = " +
                      str(returned_donate_count) + "\033[0m")
            else:
                self.test_results[self.current_student_index][self.SPECIAL_DONATE_CHECK_DONATE_COUNT] = 1
                self.test_results[self.current_student_index][self.SPECIAL_DONATE_STUDENT_NUMBER_WEI] = 1
        except Exception as e:
            print("\033[0;31;40mException special_donate_test donate student number wei:\n    " + str(e) + "\033[0m")
            return_value = False

        try:
            # Exceed donate studentNumber wei from participant address
            temp_value = int(self.students.students_list[self.current_student_index][self.students.STUDENT_NUMBER_INDEX])
            self.send_wei_to_contract_donate(temp_value, "wei", participant_address)

            # Check if the totalDonateValue has been updated correctly
            return_value = False
            print(
                "\033[0;31;40mTest case donate_test " + str(temp_value) +
                " wei overflow failure:\n    expected_error_message = " +
                self.TOTAL_DONATES_EXCEEDS_FUNDING_GOAL + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(expected_error_message):
                # if you find the same code means the function is correct
                return_value = True
                self.test_results[self.current_student_index][self.SPECIAL_DONATE_OVER_2] = 1
            else:
                return_value = False
                print("\033[0;31;40mTest case special_donate_test " + str(temp_value) +
                      " wei overflow failure:\n    expected_error_message = " +
                      expected_error_message + "\033[0m")
                print("\033[0;31;40m    returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        return return_value

    def withdraw_test(self):
        return_value = True

        try:
            # None beneficiary withdraw
            participant_address = self.config.configuration[Configuration.ACCOUNTS]
            [CrowdTest.NONE_BENEFICIARY_ADDRESS_INDEX][Configuration.ADDRESS]
            self.withdraw(1, participant_address)

            return_value = False
            print(
                "\033[0;31;40mTest case withdraw by not beneficiary failure:\n    expected_error_message = " +
                self.ONLY_BENEFICIARY_CAN_CALL + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(self.ONLY_BENEFICIARY_CAN_CALL):
                # if you find the ONLY_BENEFICIARY_CAN_CALL means the function is correct
                self.test_results[self.current_student_index][self.WITHDRAW_NONE_BENEFICIARY] = 1
                return_value = True
            else:
                return_value = False
                print("\033[0;31;40mTest case withdraw by not beneficiary failure:\n    expected_error_message = " +
                      self.ONLY_BENEFICIARY_CAN_CALL + "\033[0m")
                print("\033[0;31;40m    returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        try:
            # Withdraw 3 ether
            participant_address = self.config.configuration[Configuration.ACCOUNTS][CrowdTest.BENEFICIARY_ADDRESS_INDEX][
                Configuration.ADDRESS]
            self.withdraw(3000000000000000000, participant_address)

            # Withdraw value is not enough
            return_value = False
            print(
                "\033[0;31;40mTest case withdraw 3 ether overflow failure:\n    expected_error_message = " +
                self.THE_BALANCE_IS_NOT_ENOUGH + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(self.THE_BALANCE_IS_NOT_ENOUGH):
                # if you find the THE_BALANCE_IS_NOT_ENOUGH means the function is correct
                self.test_results[self.current_student_index][self.WITHDRAW_OVER] = 1
                return_value = True
            else:
                return_value = False
                print("\033[0;31;40mTest case withdraw 3 ether overflow failure:\n    expected_error_message = " +
                      self.THE_BALANCE_IS_NOT_ENOUGH + "\033[0m")
                print("\033[0;31;40m    returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        try:
            # Withdraw 2 ether
            participant_address = self.config.configuration[Configuration.ACCOUNTS][CrowdTest.BENEFICIARY_ADDRESS_INDEX][
                Configuration.ADDRESS]
            self.withdraw(2000000000000000000, participant_address)

            # Withdraw value is not enough
            return_value = False
            print(
                "\033[0;31;40mTest case withdraw 2 ether equal failure:\n    expected_error_message = " +
                self.THE_BALANCE_IS_NOT_ENOUGH + "\033[0m")
            print(
                "\033[0;31;40m    No error message returned\033[0m")
        except Exception as e:
            returned_error_message = str(e)

            if returned_error_message.find(self.THE_BALANCE_IS_NOT_ENOUGH):
                # if you find the THE_BALANCE_IS_NOT_ENOUGH means the function is correct
                self.test_results[self.current_student_index][self.WITHDRAW_EQUAL] = 1
                return_value = True
            else:
                return_value = False
                print("\033[0;31;40mTest case withdraw 2 ether equal failure:\n    expected_error_message = " +
                      self.THE_BALANCE_IS_NOT_ENOUGH + "\033[0m")
                print("\033[0;31;40m    returned_error_message = " +
                      returned_error_message.split("'")[1] + "\033[0m")

        try:
            initial_balance = self.web3.eth.getBalance(self.current_contract.address)
            participant_address = self.config.configuration[Configuration.ACCOUNTS][CrowdTest.BENEFICIARY_ADDRESS_INDEX][
                Configuration.ADDRESS]

            # Withdraw studentNumber wei from participant address
            temp_value = int(self.students.students_list[self.current_student_index][self.students.STUDENT_NUMBER_INDEX])
            self.withdraw(temp_value, participant_address)

            # Check if the totalDonateValue has been updated correctly
            returned_total_donate_value = self.current_contract.functions.totalDonateValue().call()
            self.expect_total_donate_value -= temp_value

            if returned_total_donate_value != self.expect_total_donate_value:
                return_value = False
                print("\033[0;31;40mTest case withdraw " + str(temp_value) +
                      " wei overflow failure:\n    expected_total_donate_value = " +
                      str(self.expect_total_donate_value) + " wei\033[0m")
                print("\033[0;31;40m    returned_total_donate_value = " +
                      str(returned_total_donate_value) + " wei\033[0m")

            # Check if the contract balance has been updated correctly
            returned_contract_balance = self.web3.eth.getBalance(self.current_contract.address)
            expected_contract_balance = initial_balance - temp_value

            if returned_contract_balance != expected_contract_balance:
                return_value = False
                print("\033[0;31;40mTest case withdraw " + str(temp_value) +
                      " wei overflow failure:\n    expected_beneficiary_balance = " +
                      str(expected_contract_balance) + " ether\033[0m")
                print("\033[0;31;40m    returned_beneficiary_balance = " +
                      str(returned_contract_balance) + " ether\033[0m")

            if return_value:
                self.test_results[self.current_student_index][self.WITHDRAW_STUDENT_NUMBER_WEI] = 1
        except Exception as e:
            print("\033[0;31;40mException withdraw student number wei:\n    "
                  + str(e) + "\033[0m")
            return_value = False

        return return_value

    def execute(self):
        print("Executing test case.")
        return_value = True
        self.donate_count = 0
        self.expect_total_donate_value = 0

        try:
            return_value &= self.donate_test()
            return_value &= self.special_donate_test()
            return_value &= self.withdraw_test()

            if return_value:
                print("Executed successfully.")
        except Exception as e:
            print("\033[0;31;40mException:\n    " + str(e) + "\033[0m")
            return_value = False
        return return_value


# python CrowdTest.py -c configuration\ConfigurationCrowd.json > .\TestResultCrowd.txt
if __name__ == "__main__":
    contract_test = CrowdTest()
    contract_test.run()
