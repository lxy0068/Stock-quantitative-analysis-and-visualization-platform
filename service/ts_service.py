#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
TuShare 接口封装
"""
import time
import tushare as ts
from service import get_ts_token

token_idx = 0
ts.set_token(get_ts_token(token_idx))
pro = ts.pro_api()


def get_stock_daily_price(stock_code, start_date, end_date):
    """
    获取股票的日线行情数据
    """
    global pro, token_idx
    stock_df = None
    while True:
        try:
            stock_df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        except:
            token_idx += 1
            ts_token = get_ts_token(token_idx)
            if ts_token:
                ts.set_token(ts_token)
                pro = ts.pro_api()
                stock_df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
            else:
                time.sleep(61)
                token_idx = 0
        if stock_df is not None:
            break

    return stock_df
