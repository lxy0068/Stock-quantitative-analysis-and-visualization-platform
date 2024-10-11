#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""

运行基金历史数据爬虫，抓取：

1、公募基金列表，以 C 类为例
2、公募基金历史净值
"""
import time
import os
from datetime import datetime, timedelta
import tushare as ts
from tqdm import tqdm
from util import get_ts_token


# token 从 github 搜索代码 pro.fund_basic()
token_idx = 0
ts_token = get_ts_token(token_idx)
ts.set_token(ts_token)
pro = ts.pro_api()

# 爬取的日期
cur_date = datetime.now()
print('爬取日期：{}'.format(cur_date))

# ----------- 爬取公募基金列表 -----------
print('爬取公募基金列表...')
fund_list_file = os.path.join(os.getcwd(), '../数据集', '公募基金列表', '{}.csv'.format(cur_date.strftime('%Y-%m-%d')))
# market: 交易市场, E场内 O场外（默认E）
# status: 存续状态 D摘牌 I发行 L上市中
funds = pro.fund_basic(market='O', status='L')
funds = funds[(funds['fund_type'] == '混合型') | (funds['fund_type'] == '股票型')]
# 同只基金，只关注 C 类的，节省运行时间
funds['is_C'] = funds['name'].map(lambda name: 'A' not in name)
funds = funds[funds['is_C'] == True].reset_index(drop=True)
del funds['is_C']
funds.to_csv(fund_list_file, index=False, encoding='utf8')
print('done.')

# ----------- 爬取公募基金历史净值 -----------
print('爬取公募基金历史净值...')
# 抽取过去 100 天的数据
for i, row in tqdm(funds.iterrows(), total=funds.shape[0]):
    fund_name = row['name']
    fund_code = row['ts_code']
    fund_file = os.path.join(os.getcwd(), '../数据集', '公募基金净值',
                             '{}({}).csv'.format(row['name'].replace('/', '_'), fund_code))

    fund_df = None
    while True:
        try:
            fund_df = pro.fund_nav(ts_code=fund_code)
        except:
            token_idx += 1
            ts_token = get_ts_token(token_idx)
            if ts_token:
                ts.set_token(ts_token)
                pro = ts.pro_api()
                fund_df = pro.fund_nav(ts_code=fund_code)
            else:
                time.sleep(61)
                token_idx = 0
        if fund_df is not None:
            break

    fund_df.to_csv(fund_file, index=False, encoding='utf8')
print('done.')
