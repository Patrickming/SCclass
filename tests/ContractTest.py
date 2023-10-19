import getopt
from typing import Tuple

import json5
import os
import sys
from abc import ABC, abstractmethod
import shutil
import solcx
from web3 import Web3
import platform
from StudentsList import Students


# Class ContractTest is base class which implements general test behaviours.
# Each inherited class of ContractTest implements special test behaviours for each contract or solidity file.
class ContractTest(ABC):
    STUDENT_NUMBER_FLAG_INDEX = 0
    FILE_CHECK_FLAG_INDEX = 1
    COMPILE_FLAG_INDEX = 2
    DEPLOY_FLAG_INDEX = 3
    RETURN_STRING_FLAG_INDEX = 4

    def __init__(
            self,
            # contract_test_file_name="",
            # solidity_files=[],
            # libraries=[[None, None]],
            # contracts=[],
            configuration=None
    ):
        self.configuration = Configuration(os.path.basename(__file__))
        configuration = self.configuration
        self.config = configuration
        self.contract_test_name=self.configuration.CONTRACT_NAME
        # ContractTest.__init__(self, self.configuration)
        # self.contract_test_sol = contract_test_file_name
        self.students = Students()

        self.check_create_log_folder()

        # self.contract_test_case_sol = self.contract_test_name + "_test.sol"
        self.contract_test_case_current_sol = ""
        self.current_compiled_sol = None

        self.web3 = Web3(Web3.HTTPProvider(self.config.node_address_port))
        self.test_results = []

        print("################################################################################")
        print("Operating System version     : " + platform.platform())
        print("Operating System architecture: " + str(platform.architecture()))
        print("CPU                          : " + platform.processor())
        print("Python version               : " + platform.python_version())
        print("Solidity compiler version    : " + self.config.solc_version)
        print("Block chain node             : " + self.config.node_address_port)
        print("")

        if self.web3.isConnected():
            # print("Debug: web3.eth.accounts = " + str(self.web3.eth.accounts))
            print("Block chain node connected.")
        else:
            print("\033[0;31;40mTest framework failure: Failed to connect block chain node " +
                  self.config.node_address_port + "\033[0m")
            print("################################################################################")
            exit(-1)

        self.current_contract = None
        self.current_student_index = 0
        self.checkSolcxVersion()

        # Shall install solc when executing test first time
        # solcx.install_solc(self.config.solc_version)

        pass

    def checkSolcxVersion(self):  # 检查是否需要下载编译器
        versions = solcx.get_installed_solc_versions()
        flag = False  # 是否需要下载编译器的判断变量
        if len(versions) == 0:
            flag = True
        for item in versions:
            if item == self.config.solc_version:
                flag = True
                break
        if flag:
            solcx.install_solc(self.config.solc_version)
        pass

    def prepare_test_environment(self):
        pass

    def check_create_log_folder(self):
        path = self.config.configuration[Configuration.LOG_FOLDER]

        if not os.path.exists(path):
            os.makedirs(path)

    # @abstractmethod
    def generate(self, student):
        print("Generate test case solidity file.")
        self.contract_test_case_current_sol = self.contract_test_name + "_" + student[0] + "_test.sol"
        shutil.copyfile(self.contract_test_case_sol, self.contract_test_case_current_sol)

        try:
            fp = open(self.contract_test_case_current_sol, 'r+')
            lines = fp.readlines()
            fp.close()
            fp = open(self.contract_test_case_current_sol, 'w+')

            for line in lines:
                new_line = line

                if line.find("StudentNumber"):
                    new_line = line.replace("StudentNumber", student[0])

                if line.find('string memory expectedString = ""'):
                    new_line = new_line.replace(
                        'string memory expectedString = ""',
                        'string memory expectedString = "Hello World! My name is Zhang San."')

                fp.write(new_line)

            fp.close()
            return True
        except OSError as e:
            return False

    def compile(self):
        print("Compiling solidity file.")
        return_value = False

        try:
            self.current_compiled_sol = solcx.compile_files(
                # self.config.configuration[Configuration.SOLIDITY_FILES][Configuration.FILE_NAME].solidity_files,
                [item[Configuration.FILE_NAME] for item in self.config.configuration[Configuration.SOLIDITY_FILES]],
                output_values=["abi",
                               # "bin-runtime"],
                               "bin"],
                solc_version=self.config.solc_version
            )
            if self.current_compiled_sol is not None:
                return_value = True
                print("Compiled successfully.")
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return return_value

    def deploy_contract(self, contract_abi, contract_bin, eoa_index):
        result = False
        contract_address = None

        try:
            self.current_contract = self.web3.eth.contract(
                abi=contract_abi,
                bytecode=contract_bin
            )
            # print("Debug: self.current_contract = " + str(self.current_contract))
            nonce = self.web3.eth.getTransactionCount(
                self.config.configuration[Configuration.ACCOUNTS][eoa_index][Configuration.ADDRESS])
            # print("Debug: eth.chain_id = " + str(self.web3.eth.chain_id))
            # print("Debug: eth.gas_price = " + str(self.web3.eth.gas_price))
            # print("Debug: nonce = " + str(nonce))
            transaction = self.current_contract.constructor().buildTransaction(
                {
                    # "chainId": chain_id,
                    "gas": 30000000,
                    "gasPrice": self.web3.eth.gas_price,
                    "from": self.config.configuration[Configuration.ACCOUNTS][eoa_index][Configuration.ADDRESS],
                    "nonce": nonce,
                }
            )
            sign_transaction = self.web3.eth.account.sign_transaction(
                transaction,
                private_key=self.config.configuration[Configuration.ACCOUNTS][eoa_index][Configuration.PRIVATE_KEY]
            )
            # print("Debug: transaction = " + str(transaction))
            # print("Debug: sign_transaction = " + str(sign_transaction))
            transaction_hash = self.web3.eth.send_raw_transaction(sign_transaction.rawTransaction)
            # Wait for the transaction to be mined, and get the transaction receipt
            transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)
            self.current_contract = self.web3.eth.contract(
                address=transaction_receipt.contractAddress,
                abi=contract_abi
            )
            # print("Debug: transaction_receipt = " + str(transaction_receipt))
            print("    Deployed address: " + transaction_receipt.contractAddress)
            contract_address = transaction_receipt.contractAddress
            result = True
        # except ValueError as e:
        #     print("ValueError: " + str(e))
        # except Web3.exceptions.ContractLogicError as e:
        #     print("ContractLogicError: " + str(e))
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return result, contract_address

    def deploy_libraries(self):
        print("Deploying solidity libraries.")
        result = False
        library = None

        if len(self.config.configuration[Configuration.COPIED_FILES]) > 0:
            for library in self.config.configuration[Configuration.LIBRARIES]:
                key_pattern = library[Configuration.FILE_NAME] + ":" + library[Configuration.LIBRARY_NAME]

                for key in self.current_compiled_sol.keys():
                    if key.find(key_pattern) >= 0:
                        print("    Deploying " + library[Configuration.LIBRARY_NAME])
                        result, library_address = self.deploy_contract(
                            self.current_compiled_sol[key]["abi"],
                            self.current_compiled_sol[key]["bin"],
                            0
                        )

                        if result:
                            library[Configuration.LIBRARY_ADDRESS] = library_address
                            library[Configuration.LIBRARY_KEY] = key
                        else:
                            break

                if not result:
                    break

            if result:
                print("Deployed solidity libraries.")
        else:
            result = True

        return result

    def deploy_contracts(self):
        print("Deploying solidity contracts.")
        result = False

        for contract in self.config.configuration[Configuration.CONTRACTS]:
            key_pattern = contract[Configuration.FILE_NAME] + ":" + contract[Configuration.CONTRACT_NAME]

            for key in self.current_compiled_sol.keys():
                if key.find(key_pattern) >= 0:
                    linked_bytecode = ""

                    if Configuration.LIBRARIES in contract and len(contract[Configuration.LIBRARIES]) > 0:
                        for library in contract[Configuration.LIBRARIES]:
                            for deployed_library in self.config.configuration[Configuration.LIBRARIES]:
                                if library[Configuration.LIBRARY_NAME] == deployed_library[Configuration.LIBRARY_NAME]:
                                    library_address = deployed_library[Configuration.LIBRARY_ADDRESS]
                                    # TODO: solcx.link_code can't convert unlinked_bytecode correctly,
                                    #  have to operate bytecode directly
                                    unlinked_bytecode = self.current_compiled_sol[key]["bin"]
                                    linked_bytecode = solcx.link_code(
                                        unlinked_bytecode,
                                        {deployed_library[Configuration.LIBRARY_KEY]: library_address}
                                    )
                                    # unlinked_bytecode = self.current_compiled_sol[key]["bin"].split("__")
                                    #
                                    # if len(unlinked_bytecode) < 2:
                                    #     linked_bytecode = self.current_compiled_sol[key]["bin"]
                                    # else:
                                    #     linked_bytecode = unlinked_bytecode[0] + \
                                    #                       library_address.split("0x")[1] + \
                                    #                       unlinked_bytecode[2]
                                    # linked_bytecode = self.link_code(
                                    #     deployed_library[Configuration.FILE_NAME],
                                    #     deployed_library[Configuration.LIBRARY_NAME],
                                    #     self.current_compiled_sol[key]["bin"],
                                    #     library_address)
                    else:
                        linked_bytecode = self.current_compiled_sol[key]["bin"]
                        pass

                    print("    Deploying " + contract[Configuration.CONTRACT_NAME])
                    result, contract_address = self.deploy_contract(
                        self.current_compiled_sol[key]["abi"],
                        linked_bytecode,
                        0
                    )

                    if result:
                        contract[Configuration.CONTRACT_ADDRESS] = contract_address
                    else:
                        break

            if not result:
                break

        if result:
            print("Deployed solidity contracts.")
        return result

    # @abstractmethod
    def deploy(self):
        return_value = self.deploy_libraries()
        return_value = return_value & self.deploy_contracts()

        return return_value

    def init_test_result(self, test_result):
        test_result.append(0)
        pass

    def check_read_word(self, read_str: str) -> bool:
        return True

    @abstractmethod
    def judge(self) -> Tuple[bool, object, object]:
        pass

    def execute(self):
        print("Executing test case.")
        return_value = False

        # Call
        try:
            res, returned_string, expected_string = self.judge()
            print("retrunstr:", returned_string)
            if res:
                return_value = True
                self.test_results[self.current_student_index][ContractTest.RETURN_STRING_FLAG_INDEX] = 1
                print("Executed successfully.")
            else:
                print("\033[0;31;40mTest case failure: expected_string = " + expected_string + "\033[0m")
                print("\033[0;31;40m                   returned_string = " + returned_string + "\033[0m")
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return return_value

    def clear(self):
        print("Clear test case solidity file.")
        return True



    def check_files(self, index):
        result = False
        file_index = 0
        full_path_name = ""

        for file in self.config.configuration[Configuration.SOLIDITY_FILES]:
            full_path_name = os.path.join("..", self.students.contracts_folder_name)
            full_path_name = os.path.join(
                full_path_name,
                self.students.students_list[index][Students.STUDENT_NUMBER_INDEX]
            )
            file_name = file[Configuration.FILE_NAME].split("\\")[-1]
            full_path_name = os.path.join(
                full_path_name,
                file_name
            )
            # 获取当前脚本的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建相对路径文件的绝对路径,方便排错
            full_path_name = os.path.join(current_dir, full_path_name)

            file[Configuration.FILE_NAME] = full_path_name
            if os.path.exists(full_path_name):
                fileCheck = open(full_path_name, "r", encoding="utf-8")
                strRead = fileCheck.read()
                # self中的在部署前进行白盒检查，如果为True继续部署，为False则终止
                result = self.check_read_word(strRead)
                if not result:
                    print("\033[0;31;40mInvalid str.\033[0m")
                    break
            else:
                print("\033[0;31;40mTest case failure: Solidity file %s does not exist.\033[0m" %
                      full_path_name)
                result = False
                break

            file_index = file_index + 1

        # return result, self.config.configuration[Configuration.SOLIDITY_FILES][file_index][Configuration.FILE_NAME]
        return result, full_path_name

    def output_test_results(self):
        test_result_file_path = os.path.join(
            self.config.configuration[Configuration.LOG_FOLDER],
            self.config.configuration[Configuration.TEST_RESULT_FILE])
        test_result_file = open(test_result_file_path, 'w')
        test_result_file.write(str(self.test_results))
        test_result_file.close()
        pass

    def copy_files_from_tests(self, student_index):
        if self.config.configuration[Configuration.COPIED_FILES]:
            for copiedFile in self.config.configuration[Configuration.COPIED_FILES]:
                source_path = os.path.join("..", "tests")
                source_path = os.path.join(source_path, copiedFile[Configuration.FILE_NAME])
                destination_path = os.path.join("..", "contracts")
                destination_path = os.path.join(
                    destination_path,
                    self.students.students_list[student_index][Students.STUDENT_NUMBER_INDEX]
                )
                destination_path = os.path.join(destination_path, copiedFile[Configuration.FILE_NAME])
                shutil.copyfile(source_path, destination_path)
                pass
        pass

    def remove_files_copied(self, student_index):
        if self.config.configuration[Configuration.COPIED_FILES]:
            for copiedFile in self.config.configuration[Configuration.COPIED_FILES]:
                destination_path = os.path.join("..", "contracts")
                destination_path = os.path.join(
                    destination_path,
                    self.students.students_list[student_index][Students.STUDENT_NUMBER_INDEX]
                )
                destination_path = os.path.join(destination_path, copiedFile[Configuration.FILE_NAME])
                os.remove(destination_path)
                pass
        pass

    # loop students list.
    # compile, deploy and execute test for the contract of each student
    def run(self):
        print("################################################################################")
        print("Staring test for " + self.contract_test_name)
        print("################################################################################")
        total_students_count = 0
        total_students_count_success = 0

        for index in range(len(self.students.students_list)):

            # [Student_Number, File_Check_Flag, Compile_Flag, Deploy_Flag]
            temp_result = [self.students.students_list[index][Students.STUDENT_NUMBER_INDEX], 0, 0, 0]
            self.init_test_result(temp_result)
            self.test_results.append(temp_result)

            if self.config.class_number is not None and \
                    self.config.class_number != \
                    self.students.students_list[index][Students.STUDENT_CLASS_NUMBER_INDEX]:
                continue

            if self.config.group_number is not None and \
                    self.config.group_number != \
                    self.students.students_list[index][Students.STUDENT_GROUP_NUMBER_INDEX]:
                continue

            if self.config.student_number is not None and \
                    self.config.student_number != \
                    self.students.students_list[index][Students.STUDENT_NUMBER_INDEX]:
                continue

            total_students_count = total_students_count + 1

            if index != 0:
                print("--------------------------------------------------------------------------------")

            print(self.students.students_list[index][Students.STUDENT_NUMBER_INDEX] + " " +
                  self.students.get_name(index) + ":")
            self.current_student_index = index
            self.copy_files_from_tests(index)
            check_result, file_name = self.check_files(index)

            # check contract to be test whether exists
            if not check_result:

                self.remove_files_copied(index)
                continue
            # generate test case files
            # elif not self.generate(student):
            #     print("\033[0;31;40mTest framework failure: Failed to generate individual contract file.\033[0m")
            #     continue
            # compile contract to be test
            elif not self.compile():
                self.test_results[self.current_student_index][ContractTest.FILE_CHECK_FLAG_INDEX] = 1
                print("\033[0;31;40mTest framework failure: Failed to compile contract file.\033[0m")
                self.remove_files_copied(index)
                continue
            # deploy contract on block chain
            elif not self.deploy():
                self.test_results[self.current_student_index][ContractTest.FILE_CHECK_FLAG_INDEX] = 1
                self.test_results[self.current_student_index][ContractTest.COMPILE_FLAG_INDEX] = 1
                print("\033[0;31;40mTest framework failure: Failed to deploy contract file.\033[0m")
                self.remove_files_copied(index)
                continue
            # execute test cases implemented in inherited class of ContractTest
            elif not self.execute():
                self.test_results[self.current_student_index][ContractTest.FILE_CHECK_FLAG_INDEX] = 1
                self.test_results[self.current_student_index][ContractTest.COMPILE_FLAG_INDEX] = 1
                self.test_results[self.current_student_index][ContractTest.DEPLOY_FLAG_INDEX] = 1
                print("\033[0;31;40mTest case failure: Failed to execute contract.\033[0m")
                self.remove_files_copied(index)
                continue
            # remove all temporary files
            # elif not self.clear():
            #     print("Test framework failure: Failed to clear generated file.")
            #     continue
            else:
                self.test_results[self.current_student_index][ContractTest.FILE_CHECK_FLAG_INDEX] = 1
                self.test_results[self.current_student_index][ContractTest.COMPILE_FLAG_INDEX] = 1
                self.test_results[self.current_student_index][ContractTest.DEPLOY_FLAG_INDEX] = 1
                total_students_count_success = total_students_count_success + 1
                self.remove_files_copied(index)

        self.output_test_results()
        print("--------------------------------------------------------------------------------")
        print("Total count of test contracts: %d" % total_students_count)
        print("Count of successful contracts: %d" % total_students_count_success)


# Class Configuration is used to parse configuration in Configuration.json
class Configuration:
    # The value of below class members shall match the corresponding key in Configuration.json
    SOLC_VERSION = 'solcVersion'
    CLASS_NUMBER = 'classNumber'
    GROUP_NUMBER = 'groupNumber'
    STUDENT_NUMBER = 'studentNumber'
    NODE_ADDRESS_PORT = 'nodeAddressPort'

    ACCOUNTS = 'accounts'
    ADDRESS = 'address'
    PRIVATE_KEY = 'privateKey'

    COPIED_FILES = 'copiedFiles'

    LOG_FOLDER = 'logFolder'

    TEST_RESULT_FILE = 'testResultFile'

    SOLIDITY_FILES = 'solidityFiles'
    FILE_NAME = 'fileName'

    LIBRARIES = 'libraries'
    LIBRARY_NAME = 'libraryName'
    # Library key (full path:library name)
    LIBRARY_KEY = 'libraryKey'
    LIBRARY_ADDRESS = 'libraryAddress'
    # FILE_NAME = 'fileName'

    CONTRACTS = 'contracts'
    CONTRACT_NAME = 'contractName'
    CONTRACT_ADDRESS = 'contractAddress'

    # LIBRARIES = 'libraries'
    # LIBRARY_NAME = 'libraryName'

    def __init__(self, test_file_name='ContractTest.py'):
        self.test_file_name = test_file_name
        self.configuration_file_name = 'Configuration_2023.json'
        self.configuration = None
        self.class_number = None
        self.group_number = None
        self.student_number = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hc:", ["configurationfile="])
        except getopt.GetoptError:
            print(test_file_name + ' -c <configurationfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print(test_file_name + ' -c <configurationfile>')
                sys.exit()
            elif opt in ("-c", "--configurationfile"):
                self.configuration_file_name = arg

        try:
            configuration_file = open(self.configuration_file_name, )
            self.configuration = json5.load(configuration_file)
            print(self.configuration)
            configuration_file.close()
        except IOError as e:
            print("\033[0;31;40mTest framework failure: Failed to load configuration file.\033[0m")
            print("\033[0;31;40m                        " + str(e) + "\033[0m")
            sys.exit(2)
        except Exception as e:
            print("\033[0;31;40mTest framework failure: Failed to load configuration file.\033[0m")
            print("\033[0;31;40m                        " + str(e) + "\033[0m")
            sys.exit(2)

        if Configuration.CLASS_NUMBER in self.configuration:
            self.class_number = self.configuration[Configuration.CLASS_NUMBER]

        if Configuration.GROUP_NUMBER in self.configuration:
            self.group_number = self.configuration[Configuration.GROUP_NUMBER]

        if Configuration.STUDENT_NUMBER in self.configuration:
            self.student_number = self.configuration[Configuration.STUDENT_NUMBER]

        if Configuration.NODE_ADDRESS_PORT in self.configuration:
            self.node_address_port = self.configuration[Configuration.NODE_ADDRESS_PORT]
        else:
            print("\033[0;31;40mTest framework failure: Missed configuration item in configuration file.\033[0m")
            print("\033[0;31;40m                        " + Configuration.NODE_ADDRESS_PORT + "\033[0m")
            sys.exit(2)

        if Configuration.SOLC_VERSION in self.configuration:
            self.solc_version = self.configuration[Configuration.SOLC_VERSION]
        else:
            print("\033[0;31;40mTest framework failure: Missed configuration item in configuration file.\033[0m")
            print("\033[0;31;40m                        " + Configuration.SOLC_VERSION + "\033[0m")
            sys.exit(2)

        if Configuration.SOLIDITY_FILES not in self.configuration:
            print("\033[0;31;40mTest framework failure: Missed configuration item in configuration file.\033[0m")
            print("\033[0;31;40m                        " + Configuration.SOLIDITY_FILES + "\033[0m")
            sys.exit(2)
        elif len(self.configuration[Configuration.SOLIDITY_FILES]) == 0:
            print("\033[0;31;40mTest framework failure: Missed configuration item in configuration file.\033[0m")
            print(
                "\033[0;31;40m                        " + Configuration.SOLIDITY_FILES + " has no solidity file item.\033[0m")
            sys.exit(2)

        if Configuration.CONTRACTS not in self.configuration:
            print("\033[0;31;40mTest framework failure: Missed configuration item in configuration file.\033[0m")
            print("\033[0;31;40m                        " + Configuration.CONTRACTS + "\033[0m")
            sys.exit(2)
        elif len(self.configuration[Configuration.CONTRACTS]) == 0:
            print("\033[0;31;40mTest framework failure: Missed configuration item in configuration file.\033[0m")
            print("\033[0;31;40m                        " + Configuration.CONTRACTS + " has no contract item.\033[0m")
            sys.exit(2)
