#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
运行股票历史数据爬虫，抓取：

1、股票列表
2、股票历史价格数据
"""
import time
import os
from datetime import datetime, timedelta
import tushare as ts
from tqdm import tqdm
from util import get_ts_token
import pandas as pd


# token 从 github 搜索代码 pro.fund_basic()
token_idx = 0
ts_token = get_ts_token(token_idx)
ts.set_token(ts_token)
pro = ts.pro_api()

# 爬取的日期
cur_date = datetime.now()
print('爬取日期：{}'.format(cur_date))

# ----------- 爬取上市公司列表 -----------
print('爬取上市公司列表...')
stock_list_file = os.path.join(os.getcwd(), '../数据集', '股票列表', '{}.csv'.format(cur_date.strftime('%Y-%m-%d')))
# list_status: 上市状态： L上市 D退市 P暂停上市，默认L
# exchange: 交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
stocks = pro.stock_basic(list_status='L', exchange='', fields='ts_code,symbol,name,area,industry,market,list_date,is_hs')
stocks.to_csv(stock_list_file, index=False, encoding='utf8')
print('done.')

# 爬取过去 300 天的数据
start_date = cur_date - timedelta(days=300)
# ----------- 爬取股票的历史数据 -----------
print('爬取股票的历史数据...')
for i, row in tqdm(stocks.iterrows(), total=stocks.shape[0]):
    stock_name = row['name']
    stock_code = row['ts_code']
    stock_daily_file = os.path.join(os.getcwd(), '../数据集', '股票日线行情', '{}({}).csv'.format(stock_name, stock_code))
    if os.path.exists(stock_daily_file):
        stock_df = pd.read_csv(stock_daily_file, parse_dates=['trade_date'])
        stock_df['trade_date'] = stock_df['trade_date'].map(lambda d: d.strftime('%Y%m%d'))
        start_date_str = stock_df.iloc[0]['trade_date']
    else:
        stock_df = pd.DataFrame()
        start_date_str = start_date.strftime('%Y%m%d')

    new_stock_df = None
    while True:
        try:
            new_stock_df = pro.daily(ts_code=stock_code, start_date=start_date_str, end_date=cur_date.strftime('%Y%m%d'))
        except:
            token_idx += 1
            ts_token = get_ts_token(token_idx)
            if ts_token:
                ts.set_token(ts_token)
                pro = ts.pro_api()
                new_stock_df = pro.daily(ts_code=stock_code, start_date=start_date_str, end_date=cur_date.strftime('%Y-%m-%d'))
            else:
                time.sleep(61)
                token_idx = 0
        if new_stock_df is not None:
            break

    stock_df = pd.concat([new_stock_df, stock_df])
    stock_df = stock_df.drop_duplicates(subset=['trade_date']).reset_index(drop=True)
    stock_df.to_csv(stock_daily_file, index=False, encoding='utf8')
print('done.')
