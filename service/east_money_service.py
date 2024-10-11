#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
东方财富爬虫接口
"""
import time
import json
import requests
import pandas as pd
import util

accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'


def get_stock_realtime_data(stock_code):
    """
    获取股票的实时交易数据
    :param stock_code:
    :return:
    """
    if 'HK' in stock_code:
        return None
    # 根据stock_code判断 SH SZ
    stock_type = util.get_stock_type(stock_code)
    if '.' not in stock_code:   # 结尾不带有 sh 或 sz
        ts_code = '{}.{}'.format(stock_code, stock_type)
    else:
        ts_code = stock_code

    stock_type_code = int(stock_type == 'SH')   # SH: 1, SZ: 0

    url = 'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292&secid={}.{}&_={}'
    url = url.format(stock_type_code, util.get_east_money_code(stock_code), int(time.time() * 1000))

    headers = {
        'Accept': accept,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'intellpositionL=1152px; IsHaveToNewFavor=0; qgqp_b_id=dbe20efaab3321e948962637a37ac894; em-quote-version=topspeed; st_si=10129111187284; em_hq_fls=js; emhq_picfq=2; cowCookie=true; cowminicookie=true; EMFUND0=02-14%2016%3A09%3A53@%23%24%u535A%u65F6%u5065%u5EB7%u6210%u957F%u53CC%u5468%u5B9A%u671F%u53EF%u8D4E%u56DE%u6DF7%u5408A@%23%24009468; EMFUND1=02-14%2016%3A09%3A53@%23%24%u535A%u65F6%u4EA7%u4E1A%u7CBE%u9009%u6DF7%u5408C@%23%24010456; EMFUND2=02-15%2001%3A43%3A49@%23%24%u6731%u96C0%u4EA7%u4E1A%u81FB%u9009%u6DF7%u5408C@%23%24007494; EMFUND3=02-14%2016%3A37%3A43@%23%24%u4E1C%u5434%u884C%u4E1A%u8F6E%u52A8%u6DF7%u5408C@%23%24011240; EMFUND4=02-18%2023%3A02%3A21@%23%24%u4E2D%u91D1%u91D1%u76CAA@%23%24005022; EMFUND5=02-18%2022%3A04%3A32@%23%24%u6613%u65B9%u8FBE%u6838%u5FC3%u4F18%u52BF%u80A1%u7968A@%23%24010196; EMFUND6=02-18%2022%3A08%3A18@%23%24%u56FD%u541B%u8D44%u7BA1%u541B%u5F97%u76C8%u503A%u5238A@%23%24952020; EMFUND7=02-18%2022%3A09%3A01@%23%24%u534E%u590F%u6210%u957F%u6DF7%u5408@%23%24000001; EMFUND8=02-18%2022%3A13%3A59@%23%24%u6C38%u8D62%u946B%u4EAB%u6DF7%u5408@%23%24008723; EMFUND9=02-19 15:28:12@#$%u56FD%u6CF0%u56FD%u8BC1%u6709%u8272%u91D1%u5C5E%u884C%u4E1A%u6307%u6570%28LOF%29@%23%24160221; intellpositionT=455px; waptgshowtime=2021219; st_asi=delete; emshistory=%5B%22603501%22%2C%22603501.SH%22%2C%22%E7%AB%8B%E8%AE%AF%E7%B2%BE%E5%AF%86%22%2C%22%E9%87%91%E9%BE%99%E9%B1%BC%22%2C%22000001%22%2C%22%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85%22%5D; HAList=a-sh-603501-%u97E6%u5C14%u80A1%u4EFD%2Ca-sz-300999-%u91D1%u9F99%u9C7C%2Ca-sz-002475-%u7ACB%u8BAF%u7CBE%u5BC6%2Ca-sz-002352-%u987A%u4E30%u63A7%u80A1%2Ca-sh-601012-%u9686%u57FA%u80A1%u4EFD%2Cd-hk-00700%2Ca-sz-300122-%u667A%u98DE%u751F%u7269%2Cd-hk-06886%2Ca-sz-300815-%u7389%u79BE%u7530%2Ca-sh-603655-%u6717%u535A%u79D1%u6280%2Ca-sz-000001-%u5E73%u5B89%u94F6%u884C%2Ca-sz-002982-%u6E58%u4F73%u80A1%u4EFD; st_pvi=89273277965854; st_sp=2020-07-21%2011%3A22%3A06; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2FBK0473.html; st_sn=278; st_psi=20210219201640978-113200301201-5905396350',
        'Referer': 'http://quote.eastmoney.com/',
        'Host': 'push2.eastmoney.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf8'
    data = resp.json()['data']

    trade_date = json.loads(data['f80'])[0]['b']
    trade_date = str(trade_date)[:-4]
    data = {
        'ts_code': [ts_code],
        'trade_date': [trade_date],
        'open': [data['f46']],
        'high': [data['f44']],
        'low': [data['f45']],
        'close': [data['f39']],
        'pre_close': [data['f60']],
        'change': [data['f169']],       # 涨跌额
        'pct_chg': [data['f170']],      # 涨跌幅
        'vol': data['f47'],        # 成交量 （手）
        'amount': float(data['f48']) / 1000      # 成交额 （千元）
    }
    new_df = pd.DataFrame(data)
    return new_df
