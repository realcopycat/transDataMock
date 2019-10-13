# this script generate a list which contains user dict

import numpy as np
from random import choice


class UserGenerater:

    def __init__(self):
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
        userPool = list()

        for i in range(0, sizeA):
            accountName = choice(self.userNameClassA) + self.randomid()
            accountNum = self.makeAccountNumber()
            balance = np.random.randint(0, 99999)
            userPool.append({
                'accountName': accountName,
                'accountNum': accountNum,
                'balance': balance,
                'class': 'A',
                'history': []
            })

        for i in range(0, sizeB):
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

        for i in range(0, sizeC):
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

        for i in range(0, sizeD):
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
        firstnum = np.random.randint(1, 9)
        othernum = np.random.randint(0, 9, size=18)

        numstr = str(firstnum)
        for each in othernum:
            numstr = numstr + str(each);

        return numstr

    def randomid(self):
        strId = ''
        for each in np.random.randint(0, 9, size=4):
            strId += str(each)
        return strId


if __name__ == '__main__':
    test = UserGenerater()
    test.userPoolGenerate()
