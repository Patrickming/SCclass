import os
import random
from typing import Tuple

from ContractTest import ContractTest,Configuration





class test_temp(ContractTest):
    totalDonateValue = 0
    donateCount = 0
    # 调用部署时候的constructor函数，向里面传递受益人的地址self.config.configuration[Configuration.ACCOUNTS][0][Configuration.ADDRESS]就是受益人的地址
    def construct_contract(self,nonce,eoa_index):
        return self.current_contract.constructor(self.config.configuration[Configuration.ACCOUNTS]
                                                 [0][Configuration.ADDRESS]).buildTransaction(
                {
                    # "chainId": chain_id,
                    "gas": 30000000,
                    "gasPrice": self.web3.eth.gas_price,
                    "from": self.config.configuration[Configuration.ACCOUNTS][eoa_index][Configuration.ADDRESS],
                    "nonce": nonce,
                }
            )
    # 向donate函数转账的Python函数 number 转账的数量,uint 转账的单位: "wei" 或 "ether"
    def send_wei_to_contract_donate(self,number:int,uint:str):
        tx_hash = self.current_contract.functions.donate().transact(
            {'from': self.config.configuration[Configuration.ACCOUNTS]
                                                 [1][Configuration.ADDRESS], 'value': self.web3.toWei(number, uint)})
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash) # 收据:表示的是交易的详情，包含gas和转账金额
        # print(tx_receipt)
        wallet = self.web3.to_checksum_address(
            self.config.configuration[Configuration.ACCOUNTS][1][Configuration.ADDRESS])
        print(self.web3.eth.getBalance(wallet))
        self.web3.eth.waitForTransactionReceipt(tx_hash)
    #对donate函数的测试
    def donateTest(self, fixed_donate: int) -> str:

    #第一次捐赠可以是任意数量的以太币（1-1000），
        random_donate = random.randint(1, 1000)
        test_temp.totalDonateValue += random_donate
        test_temp.donateCount += 1
    #而第二次捐赠必须是2ETH。如果第二次捐赠超过了2ETH， 将会触发错误并显示错误信息"Total donates exceeds the funding goal."
        if fixed_donate > 2:
            return "Total donates exceeds the funding goal."
        else:
            test_temp.totalDonateValue += fixed_donate
            test_temp.donateCount += 1
        return "donate succeed."

    #对specialDonate函数的测试
    def specialDonateTest(self, special_donate: int) -> str:
    #设置最大最小特殊捐献值
        min_donate = 1000000000
        max_donate = 9999999999
    #特殊捐赠
        if special_donate < min_donate or special_donate > max_donate :
            return "Donate value is not correct, it should be {x} wei."
        else:
            test_temp.totalDonateValue += special_donate
            test_temp.donateCount += 1
            return "donate succeed."
     #随机数捐赠(1,10000)
        special_random_donate = random.randint(1,10000)

        if special_random_donate < min_donate or special_random_donate > max_donate:
            return "Donate value is not correct, it should be {x} wei."
        else:
            totalDonateValue += special_donate
            donateCount += 1
            return "donate succeed."
    #对withdraw函数的测试
    def withdrawTest(self,withdraw_value: int) -> str:
    #正常提取
        if test_temp.totalDonateValue > withdraw_value:
            test_temp.totalDonateValue -= withdraw_value
        else:
            expected_string = "The balance is not enough."
            return expected_string
    #随机数提取(剩余货币数加上1-1000随机数的)
        withdraw_random_value = random.randint(1,1000) + test_temp.totalDonateValue
        if test_temp.totalDonateValue > withdraw_random_value:
            test_temp.totalDonateValue -= withdraw_random_value
        else:
            expected_string= "The balance is not enough."
            return expected_string

    def judge(self) -> Tuple[bool, object, object,object,object,object]:
        print(self.current_contract)
        # demo调用
        # self.send_wei_to_contract_donate(2,'ether')
        fixed_donate = random.randint(1,1000)
        donateTest_message = self.donateTest(fixed_donate)
        special_donate = random.randint(1,10000)
        specialDonateTest_message = self.specialDonateTest(special_donate)
        withdraw_value = random.randint(1,1000)
        excepted_string = self.withdrawTest(withdraw_value)
        return_string = self.current_contract.functions.withdraw(withdraw_value).call()
        return return_string == excepted_string,donateTest_message,specialDonateTest_message,excepted_string,return_string
# python StringConcatTest.py -c .\Configuration_201-1.json > test_result.txt
if __name__ == "__main__":
    contract_test = test_temp()
    contract_test.run()