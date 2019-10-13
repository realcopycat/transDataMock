import pandas as pd
import random
import time
import math
import numpy as np

OUTPUT_PATH = '/Users/copycat/rawData/financialData'


class trans_generate:

    def __init__(self, total_sum=3000, user_sum=30, group_num=3, super_ratio=0.4, trans_limit=20000):
        self.total_sum = total_sum  # 总交易数
        self.user_sum = user_sum  # 总用户数
        self.super = super_ratio  # 强制交易分组的几率,越大意味着越有可能在同组交易
        # self.start_time = '2019-01-01 00:00:00'
        self.group_num = group_num  # 分组数
        self.trans_amount_limit = trans_limit
        self.per_group_num = math.floor(user_sum / group_num)  # 每组人数
        self.user_list, self.user_balance = self.user_dict_generate()  # 生成组列表，以及维护余额字典

    @staticmethod
    def account_num_generate():
        firstnum = np.random.randint(1, 9)
        othernum = np.random.randint(0, 9, size=18)

        numstr = str(firstnum)
        for each in othernum:
            numstr = numstr + str(each);

        return numstr

    def user_dict_generate(self):
        count = 0
        user_dict = dict()
        while count < self.user_sum:
            count += 1
            user_dict[trans_generate.account_num_generate()] = np.random.randint(0, 99999)  # 合成字典列表

        return list(user_dict.keys()), user_dict

    def trans_user_generate(self):
        while True:
            user1 = random.choice(self.user_list)
            user2 = random.choice(self.user_list)
            if user1 != user2:
                mod1 = int(user1) % self.per_group_num
                mod2 = int(user2) % self.per_group_num
                if mod1 == mod2:  # 如果在同组交易
                    if np.random.rand(1)[0] < self.super:  # 且满足一定比例
                        return user1, user2

                return user1, user2

    def trans_amount_generate(self):
        while True:
            amount = np.random.randint(1, self.trans_amount_limit)
            if amount > self.trans_amount_limit / 2:
                if np.random.rand(1)[0] < self.super:
                    return amount
            return amount

    def check_balance(self, out_account, amount):
        if self.user_balance[out_account] < amount:
            return False
        return True

    def trans_generate(self):
        count = 0
        trans_history = list()
        start_time = time.time()
        while count < self.total_sum:
            tmp_dict = dict()
            out_account, in_account = self.trans_user_generate()
            amount = self.trans_amount_generate()
            if self.check_balance(out_account, amount):
                continue

            tmp_dict['in_account'] = in_account
            tmp_dict['out_account'] = out_account
            tmp_dict['amount'] = amount

            trans_history.append(tmp_dict)
            end_time = time.time()
            total_time = end_time - start_time
            count += 1
            print('{0} %, total_time : {1}'.format((count / self.total_sum), total_time))

        data = pd.DataFrame(trans_history)
        data.to_csv(OUTPUT_PATH + '/test.csv')


if __name__ == '__main__':
    trans = trans_generate()
    trans.trans_generate()
