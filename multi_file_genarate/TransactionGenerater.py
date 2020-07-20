import random
import time
import datetime


class TransactionGenerater:

    def __init__(self, userList, transSum, duration=3):
        self.userList = userList  # 用户列表获取
        self.duration = duration  # 转账时间限制
        self.start_time = '2019-01-01 00:00:00'  # 起始时间限制
        self.format = '%Y-%m-%d %H:%M:%S'  # 时间格式

        self.transSum = transSum  # 交易总数
        # Process duration at first
        self.__init__processDuration()  # 初始时间设定函数

    def __init__processDuration(self):
        """
        此函数保证交易时间的发生是均匀的
        """
        startTime = datetime.datetime.strptime(self.start_time, self.format)
        self.end_time = (startTime + datetime.timedelta(days=self.duration)).strftime(self.format)

        sTime = time.mktime(time.strptime(self.start_time, self.format))
        eTime = time.mktime(time.strptime(self.end_time, self.format))

        self.TIME_DIFFERENCE = int(eTime - sTime)
        self.TIME_START_TIME = sTime
        self.TIME_CUP = self.TIME_DIFFERENCE / self.transSum
        self.timeBottle = 0

    def userPick(self):
        """
        随机选择两个交易账户
        """
        while True:
            userA = random.choice(self.userList)
            userB = random.choice(self.userList)
            if userA != userB:
                return userA, userB

    def timeStamp(self):
        """
        生成时间戳
        """
        while True:
            self.timeBottle += self.TIME_CUP
            randomStamp = self.TIME_START_TIME + self.timeBottle
            yield time.strftime(self.format, time.localtime(randomStamp))

    def randomAmount(self):
        """
        随机生成数额
        """
        limit = random.choice([50, 50, 100, 100,
                               400, 800, 3000,
                               5000, 10000, 50000])
        return random.randint(1, limit)

    def transactionRecordBuild(self):
        """
        交易摘要生成
        """
        transDict = {}  # 交易摘要字典
        account, oppositeAccount = self.userPick()  # 获取交易用户
        # trans_time = self.randomTimeStamp()

        # oppositeAccount TO account, the balance of oppositeAccount decline
        transDict['account'] = account['accountNum']  # 写入交易账户
        transDict['oppositeAccount'] = oppositeAccount['accountNum']  # 写入对方用户
        # transDict['time'] = trans_time
        transDict['amount'] = self.randomAmount()  # 写入交易金额

        return transDict
