import random
import time
import datetime


class TransactionGenerater:

    def __init__(self, userList, transSum, duration=3):
        self.userList = userList
        self.duration = duration
        self.start_time = '2019-01-01 00:00:00'
        self.format = '%Y-%m-%d %H:%M:%S'

        self.transSum = transSum
        # Process duration at first
        self.__init__processDuration()

    def __init__processDuration(self):
        startTime = datetime.datetime.strptime(self.start_time, self.format)
        self.end_time = (startTime + datetime.timedelta(days=self.duration)).strftime(self.format)

        sTime = time.mktime(time.strptime(self.start_time, self.format))
        eTime = time.mktime(time.strptime(self.end_time, self.format))

        self.TIME_DIFFERENCE = int(eTime - sTime)
        self.TIME_START_TIME = sTime
        self.TIME_CUP = self.TIME_DIFFERENCE / self.transSum
        self.timeBottle = 0

    def userPick(self):
        while True:
            userA = random.choice(self.userList)
            userB = random.choice(self.userList)
            if userA != userB:
                return userA, userB

    def timeStamp(self):
        while True:
            self.timeBottle += self.TIME_CUP
            randomStamp = self.TIME_START_TIME + self.timeBottle
            yield time.strftime(self.format, time.localtime(randomStamp))

    def randomAmount(self):
        limit = random.choice([50, 50, 100, 100,
                               400, 800, 3000,
                               5000, 10000, 50000])
        return random.randint(1, limit)

    def transactionRecordBuild(self):
        transDict = {}
        account, oppositeAccount = self.userPick()
        # trans_time = self.randomTimeStamp()

        # oppositeAccount TO account, the balance of oppositeAccount decline
        transDict['account'] = account['accountNum']
        transDict['oppositeAccount'] = oppositeAccount['accountNum']
        # transDict['time'] = trans_time
        transDict['amount'] = self.randomAmount()

        return transDict
