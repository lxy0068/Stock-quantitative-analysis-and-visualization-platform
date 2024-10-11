#!/usr/bin/python
# _*_ coding: utf-8 _*_

token_pool = ['0577694ff6087849a141deb1c12ddf8566710906b8f64548f03183ce',
              '62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d',
              'd9f49767544519208fbf91e00a109558fe92e84bdcb70c9173144c24',
              'e546fbc7cc7180006cd08d7dbde0e07f95b21293a924325e89ca504b',
              'dfb6e9f4f9a3db86c59a3a0f680a9bdc46ed1b5adbf1e354c7faa761',
              'ac147953b15f6ee963c164fc8ee8ef5228e58b75e5953ba5997ef117']


def get_ts_token(idx):
    if idx > len(token_pool):
        return None
    return token_pool[idx]


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    if stock_code.startswith(("SH", "SZ")):
        return stock_code[:2]
    if stock_code.startswith(
            ("50", "51", "60", "90", "110", "113", "132", "204")
    ):
        return "SH"
    if stock_code.startswith(
            ("00", "13", "18", "15", "16", "18", "20", "30", "39", "115", "1318")
    ):
        return "SZ"
    if stock_code.startswith(("5", "6", "9", "7")):
        return "SH"
    return "SZ"


def get_tushare_code(code):
    """
    转换为 tushare 规则的代码
    :param code:
    :return:
    """
    stock_type = get_stock_type(code)
    if '.' not in code:  # 结尾不带有 sh 或 sz
        ts_code = '{}.{}'.format(code, stock_type)
    else:
        ts_code = code
    return ts_code


def get_east_money_code(code):
    """
    转换为 eastmoney 规则的代码
    :param code:
    :return:
    """
    if '.' not in code:  # 结尾不带有 sh 或 sz
        return code
    else:
        return code.split('.')[0]
