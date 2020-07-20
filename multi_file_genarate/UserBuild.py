# this script generate a list which contains user dict

import numpy as np
from random import choice


class UserGenerater:

    def __init__(self):
        """
        本生成器内的账户有四类，
        1 支付平台
        2 银行支取等
        3 商家
        4 对公账户
        """
        self.userNameClassA = [
            "支付宝",
            "财付通",
            "某第三方支付平台"
        ]
        self.userNameClassB = [
            "中国建设银行分行",
            "农业银行分行",
            "中国工商银行",
            "中国银行分行",
            "某网商银行",
        ]
        self.userNameClassC = [
            "线下商家",
            "快捷支付单位"
        ]
        self.userNameClassD = [
            "个人账户",
            "对公账户"
        ]

    def userPoolGenerate(self, sizeA=4, sizeB=10, sizeC=9, sizeD=20):
        """
        参数为四类账户的数目
        """
        userPool = list()  # 用户总列表

        for i in range(0, sizeA):
            accountName = choice(self.userNameClassA) + self.randomid()  # 随机生成账户名
            accountNum = self.makeAccountNumber()  # 随机生成账户号码
            balance = np.random.randint(0, 99999)  # 随机赋予账户初始余额
            userPool.append({
                'accountName': accountName,
                'accountNum': accountNum,
                'balance': balance,
                'class': 'A',
                'history': []
            })  # 加入总列表中

        for i in range(0, sizeB):  # 原理同上
            accountName = choice(self.userNameClassB) + self.randomid()
            accountNum = self.makeAccountNumber()
            balance = np.random.randint(0, 99999)
            userPool.append({
                'accountName': accountName,
                'accountNum': accountNum,
                'balance': balance,
                'class': 'B',
                'history': []
            })

        for i in range(0, sizeC):  # 原理同上
            accountName = choice(self.userNameClassC) + self.randomid()
            accountNum = self.makeAccountNumber()
            balance = np.random.randint(0, 99999)
            userPool.append({
                'accountName': accountName,
                'accountNum': accountNum,
                'balance': balance,
                'class': 'C',
                'history': []
            })

        for i in range(0, sizeD):  # 原理同上
            accountName = choice(self.userNameClassD) + self.randomid()
            accountNum = self.makeAccountNumber()
            balance = np.random.randint(0, 99999)
            userPool.append({
                'accountName': accountName,
                'accountNum': accountNum,
                'balance': balance,
                'class': 'D',
                'history': []
            })

        print(userPool)
        return userPool

    def makeAccountNumber(self):
        """
        用于随机生成账户号码
        """
        firstnum = np.random.randint(1, 9)
        othernum = np.random.randint(0, 9, size=18)

        numstr = str(firstnum)
        for each in othernum:
            numstr = numstr + str(each);

        return numstr

    def randomid(self):
        """
        随机生成ID
        """
        strId = ''
        for each in np.random.randint(0, 9, size=4):
            strId += str(each)
        return strId


if __name__ == '__main__':
    test = UserGenerater()
    test.userPoolGenerate()
