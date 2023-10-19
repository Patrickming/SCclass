import random
import re
from typing import Tuple

from tests.ContractTest import ContractTest
from tests.TestAbstract import TestAbstract


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
    def judge(self) -> Tuple[bool, object, object]:
        random_age = getAge()
        age, expected_string = getAnswer(random_age)
        returned_string = self.current_contract.functions.myAge(random_age).call()
        return returned_string == expected_string, returned_string, expected_string

    def check_read_word(self, read_str: str) -> bool:
        # 要查找的字符
        character = "abi.encodePacked("
        # 构建正则表达式模式
        pattern = re.escape(character)
        # 使用 re 模块进行匹配
        match = re.search(pattern, read_str)

        return match is None


if __name__ == "__main__":
    contract_test = StringConcatTest()
    contract_test.run()
