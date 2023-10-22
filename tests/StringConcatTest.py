import os
import random
import re
from typing import Tuple

from ContractTest import ContractTest, Configuration


def getAge() -> int:
    random_age = random.randint(1, 150)
    return random_age


def getAnswer(user_age: int) -> (object, str):
    your_age = user_age
    expected_string = "My age is " + str(your_age)+"."
    return your_age, expected_string


#  在ContractTest中有两个方法支持重写:judge(self)和check_read_word(self, read_str: str)
#  不同点:
#  judge(self):每个用例的判断函数，必须强制重写
#  check_read_word(self, read_str: str): 每个用例的部署前源文件检测，不强制重写，只在需要进行检查之前(对代码文本进行检测的时候)重写，检测代码是否符合题目规范
#  TO Fix(算是一个小bug):读的时候是将文本全部读进内存，不建议进行大量的多线程操作
class StringConcatTest(ContractTest):
    RETURN_STRING_FLAG_INDEX = 4
    # NULL_STRING_COMPARE_FLAG_INDEX = 4
    COMMON_STRING_COMPARE_FLAG_INDEX = 5

    def __init__(self):
        configuration = Configuration(os.path.basename(__file__))
        ContractTest.__init__(self, configuration=configuration)
        # Set the contract name to be tested.
        self.contract_test_name = "StringConcatDemo"
        self.solidity_file = None
        pass

    def init_test_result(self, test_result):
        # RETURN_STRING_FLAG_INDEX
        test_result.append(0)
        # COMMON_STRING_COMPARE_FLAG_INDEX
        test_result.append(0)
        pass

    def judge(self) -> Tuple[bool, object, object]:
        random_age = getAge()
        age, expected_string = getAnswer(random_age)
        returned_string = self.current_contract.functions.myAge(random_age).call()
        return returned_string == expected_string, returned_string, expected_string

    def check_read_word(self, read_str: str) -> bool:
        return_value = False
        # 要查找的字符
        character = "abi.encodePacked("
        # 构建正则表达式模式
        pattern = re.escape(character)
        # 使用 re 模块进行匹配
        match = re.search(pattern, read_str)

        if match is None:
            return_value = True
        else:
            return_value = False
            print("\033[0;31;40mTest case failure: Shall not use abi.encodePacked to concat string\033[0m")

        character = ".concat("
        pattern = re.escape(character)
        match = re.search(pattern, read_str)

        if match is not None:
            return_value = False
            print("\033[0;31;40mTest case failure: Shall not use string.concat to concat string\033[0m")

        return return_value

    def execute(self):
        print("Executing test case.")
        return_value = False

        # Call
        try:
            res, returned_string, expected_string = self.judge()
            # print("retrunstr:", returned_string)
            if res:
                return_value = True
                self.test_results[self.current_student_index][StringConcatTest.RETURN_STRING_FLAG_INDEX] = 1
            else:
                print("\033[0;31;40mTest case failure: expected_string = " + expected_string + "\033[0m")
                print("\033[0;31;40m                   returned_string = " + returned_string + "\033[0m")

            file_check = open(
                self.config.configuration[Configuration.SOLIDITY_FILES][0][Configuration.FILE_NAME],
                "r",
                encoding="utf-8"
            )
            str_read = file_check.read()
            # print(str_read)

            if self.check_read_word(str_read):
                self.test_results[self.current_student_index][StringConcatTest.COMMON_STRING_COMPARE_FLAG_INDEX] = 1
            else:
                return_value = False

            file_check.close()

            if return_value:
                print("Executed successfully.")
        except Exception as e:
            print("\033[0;31;40mException: " + str(e) + "\033[0m")

        return return_value


if __name__ == "__main__":
    contract_test = StringConcatTest()
    contract_test.run()
