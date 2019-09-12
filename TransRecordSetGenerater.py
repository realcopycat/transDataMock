from UserBuild import UserGenerater
from TransactionGenerater import TransactionGenerater
import pandas as pd
import random
from numba import jit
import time

OUTPUT_PATH = '/Users/copycat/rawData/financialData'


class TransRecordSetGenerater:

    def __init__(self, totalSum):
        UserTool = UserGenerater()
        self.userPool = UserTool.userPoolGenerate(sizeA=4, sizeB=50, sizeC=30, sizeD=100)
        self.TransGenerate = TransactionGenerater(self.userPool, totalSum)
        self.timeGenerater = self.TransGenerate.timeStamp()
        self.totalSum = totalSum

        accountNumList = [x['accountNum'] for x in self.userPool]
        accountInitialBalanceList = [x['balance'] for x in self.userPool]
        self.currentBalanceDict = dict(zip(accountNumList, accountInitialBalanceList))

    def insertHistory(self):
        countSum = 0
        countCheck = 0
        countDeal = 0
        startTime = time.clock()  # initial
        # expectTime = 'unknown'  # initial

        while True:
            endTime = time.clock()
            try:
                expectTime = (((endTime - startTime) / countDeal)*(self.totalSum - countDeal)) / 60
            except ZeroDivisionError as z:
                expectTime = 'unknown'
            print('sum: {sum}, pass : {check}, deal: {deal}, {percent}%%, expect time: {expect} MINs'. \
                  format(sum=countSum, deal=countDeal, expect=expectTime,
                         check=countCheck, percent=(countDeal / self.totalSum) * 100))
            tmp_transHistory = self.TransGenerate.transactionRecordBuild()
            # print('{ 交易生成 }')
            countSum += 1
            transType = self.digestGenerateANDFliter(tmp_transHistory)
            if transType is not False:
                tmp_transHistory['type'] = transType
                # print('{ check pass }')
                countCheck += 1
            else:
                continue
            if tmp_transHistory['amount'] >= self.currentBalanceDict[tmp_transHistory['oppositeAccount']]:
                continue
            else:
                # print('{ deal ! }')
                """
                tmp_transHistory:
                    account永远是收钱的那一个
                    oppositeAccount永远是出钱的那一个
                    所以 oppositeAccount是扣钱的
                    在余额修改🐸之后 再来读取余额
                    
                """
                countDeal += 1
                self.currentBalanceDict[tmp_transHistory['oppositeAccount']] -= tmp_transHistory['amount']
                self.currentBalanceDict[tmp_transHistory['account']] += tmp_transHistory['amount']
                self.transDictBuildANDInsert(tmp_transHistory)
                # print('[ insert finish ] count:{count}'.format(count=count))
                # endTime = time.clock()
                # expectTime = ((endTime - startTime)*(self.totalSum - countDeal)) / 60
                # startTime = time.clock()
            if countDeal >= self.totalSum:
                break

    @jit
    def transDictBuildANDInsert(self, originTransDict):
        i_account = dict()
        o_account = dict()

        i_account['oppositeAccount'] = originTransDict['oppositeAccount']
        o_account['oppositeAccount'] = originTransDict['account']
        i_account['time'] = o_account['time'] = self.timeGenerater.send(None)
        i_account['balance'] = self.currentBalanceDict[originTransDict['account']]
        o_account['balance'] = self.currentBalanceDict[originTransDict['oppositeAccount']]
        i_account['amount'] = originTransDict['amount']
        o_account['amount'] = - originTransDict['amount']
        i_account['type'] = o_account['type'] = originTransDict['type']

        pos_index = 0
        for each in self.userPool:
            if each['accountNum'] == originTransDict['account']:
                o_account['oppositeAccountName'] = each['accountName']
                pos_i_account = pos_index
            if each['accountNum'] == originTransDict['oppositeAccount']:
                i_account['oppositeAccountName'] = each['accountName']
                pos_o_account = pos_index
            pos_index += 1

        self.userPool[pos_i_account]['history'].append(i_account)
        self.userPool[pos_o_account]['history'].append(o_account)

        return True

    @jit
    def printHistory(self):
        for each in self.userPool:
            eachData = pd.DataFrame(each['history'])
            eachData['time'] = pd.to_datetime(eachData['time'], format=self.TransGenerate.format)
            eachData.sort_values('time', inplace=True)
            eachData.index = range(len(eachData))
            eachData.to_csv((OUTPUT_PATH + '/' + each['accountNum'] + ',' + each['accountName'] + '.csv'))

    @jit
    def digestGenerateANDFliter(self, originTransDict):
        for each in self.userPool:
            if each['accountNum'] == originTransDict['account']:
                i_class = each['class']
            if each['accountNum'] == originTransDict['oppositeAccount']:
                o_class = each['class']

        # flit by class
        if o_class == 'D':
            if i_class == 'D':
                return '转账'
            if i_class == 'C':
                return '消费'
            if i_class == 'B':
                return random.choice(['ATM取款', '理财产品支出', '代扣', '还款'])
            if i_class == 'A':
                return random.choice(['消费', '理财基金转账', '转账'])
        if o_class == 'A':
            if (o_class == 'B') | (o_class == 'A') | (o_class == 'C'):
                return False
            if o_class == 'D':
                return random.choice(['转账', '退款'])
        if o_class == 'B':
            if o_class == 'D':
                return random.choice(['ATM存入', '电子汇入'])
            else:
                return False
        if o_class == 'C':
            return False


if __name__ == '__main__':
    test = TransRecordSetGenerater(2000)
    test.insertHistory()
    test.printHistory()
